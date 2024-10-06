import serial
import time
from KerbalSimpit.cobs import *
from KerbalSimpit.const import *


class KerbalSimpit:
    def __init__(self, port:str, baudrate:int=115200) -> None:
        """
        :param port: The port the class should listen to
        :param baudrate: The baudrate has to be equal to the baudrate of the kerbalSimpit mod. 

        
        To use it, first do a hand_shake().

        Use `register_channel(channel_id)` to get data from the game.

        Use `update(message_handler)` together with your message handler to process the incoming data.
        """
        self.port = port
        self.baudrate = baudrate

        self._ser = serial.Serial(port, baudrate=baudrate)
        self._ser.set_buffer_size(rx_size=4096, tx_size=4096)
        self.packet_dropped_num = 0
        self._inbound_buffer = list()
        self.registered_channels = []

        for _ in range(3):
            if not self._ser.is_open:
                print("Trying to connect...")
                time.sleep(1)
        if self._ser.is_open:
            print("Connected", port)
        else:
            print("Failed to connect")

    def hand_shake(self) -> bool:
        """
        In order ro send and reciv messages the program and the game need to perform a handshake.
        The function returns True if the handshake was successful and False otherwise
        """
        time.sleep(.1) # Wait for any incoming message to finnish

        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

        msg = [0x00] + list(KERBALSIMPIT_VERSION.encode("utf-8"))
        self._send(0x00, msg)

        waiting_loops = 0
        while not self._ser.in_waiting:
            if waiting_loops > 10:
                print("Error: Timout in hand shake")
                return False
            time.sleep(.1)
            waiting_loops += 1

        _inboundBuffer = []
        while self._ser.in_waiting > 0:
            _inboundBuffer.append(self._ser.read(1)[0]) 
            if _inboundBuffer[-1] == 0:
                decoded_message = cobs_decode(_inboundBuffer)
                if len(decoded_message) < 2:
                    continue
                if decoded_message[0] == 0x00 and decoded_message[1] == 0x01:
                    msg[0] = 0x02
                    self._send(0, msg)
                    return True
        return False
        

    # Funktion zum Senden einer Nachricht über den seriellen Port
    def _send(self, message_type:bytes, msg:list[bytes]):
        """
        For internal use
        """
        msg_buffer = [message_type]
        checksum = message_type
        
        # Calculate Checksum
        for byte in msg:
            msg_buffer.append(byte)
            checksum ^= byte
        
        msg_buffer.append(checksum)
        
        encoded_message = cobs_encode(msg_buffer)
        encoded_message_bytes = bytes(encoded_message)

        self._ser.write(encoded_message_bytes)  
        self._ser.write(b'\x00')  # Null-Byte (for COBS-Termination)

    def print_to_ksp(self, message_str:str):
        """
        Send a text to the game
        """
        msg = list(message_str.encode('utf-8')) 
        payload = [CustomLogStatus.PRINT_TO_SCREEN]
        for i in range(min(31, len(msg)-1)):
            payload.append(msg[i])
        payload.append(0)
        self._send(InboundPackets.CUSTOM_LOG, payload)

    def register_channel(self, channel_id:int) -> None:
        """
        Register a channel to reciv a message whenever a value on the specified channel changes

        :param channel_id: The ID of the channel. Example: `OutboundPackets.VELOCITY_MESSAGE`
        """
        self._send(InboundPackets.REGISTER_MESSAGE, [channel_id])
        self.registered_channels.append(channel_id)
        return False

    def request_messages(self):
        """
        Request messages on all registered channels
        """
        self._send(InboundPackets.REGISTER_MESSAGE, [0])

    def update(self, message_handler, print_debug=False) -> None:
        """
        Call this function in a loop. It will decode all messages in the serial buffer and pass it to the message handler.

        :param message_handler: A function that recives a message_type of type int and a message_struct containing the information sent by the game. Example: `def message_handler(message_type, message_struct):`
        :param print_debug: Send information about lost packages to the consol
        """
        # as long as data is available
        while self._ser.in_waiting > 0:
            self._inbound_buffer.append(self._ser.read(1)[0])

            # Check, if the last Byte is 0 (Null-Byte) 
            if self._inbound_buffer[-1] == 0:

                # Decode message
                decoded_message = cobs_decode(self._inbound_buffer)
                decodedSize = len(decoded_message)

                # Check if message body is not empty
                if decodedSize < 2:
                    if print_debug:
                        print(f"Error: Short message {decoded_message}")
                    self._inbound_buffer = list()
                    return
                
                # Check decoded message's size
                if decodedSize != len(self._inbound_buffer) - 1:
                    if print_debug:
                        print(f"Error: decodedSize does not match {decodedSize=} {len(self._inbound_buffer)=} {self._inbound_buffer=}")
                    self.packet_dropped_num += 1
                    self._inbound_buffer = list()
                    return
                
                # Calculate Checksum
                calculated_checksum = 0
                for x in range(decodedSize - 2):
                    calculated_checksum ^= decoded_message[x]
                
                # Verify Checksum
                message_checksum = decoded_message[-2]
                if calculated_checksum != message_checksum:
                    if print_debug:
                        print(f"Error in Checksum: {calculated_checksum=} {message_checksum=} {decoded_message=}")
                    self.packet_dropped_num += 1
                    self._inbound_buffer = list()
                    return
                
                message_handler(decoded_message[0], decoded_message[1:-2])
                self._inbound_buffer = list()
                
    def close(self, close_signal=False):
        """
        Close the serial connection

        :param close_signal: sends a close signal to the game, to close the connection on the game side as well. Default `False`
        """
        print("Deregister channels")
        for channel_id in self.registered_channels:
            self._send(InboundPackets.DEREGISTER_MESSAGE, [channel_id])
        if close_signal:
            print("Send close serial")
            self._send(InboundPackets.CLOSE_SERIAL, [0])
        print("Closing serial connection")
        self._ser.close()

