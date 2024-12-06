/*
This program is a UART Communication Task, that send and receive data between Atmega328p and PC.
This task is created for Nymble Firmware Engineer Role Assignment
Program Created by Jim Castro Soman
*/

// Libirary Import
#include <avr/io.h>
#include <util/delay.h>
#include <avr/eeprom.h>

#define BaudRate 2400
#define EEPROM_SIZE 1024 // Atmega328p EEPROM Size
bool memory = false; // momory leak flag

// UART init
void uart_init(unsigned int baud) 
{
  unsigned int ubrr = (F_CPU / (16 * baud)) - 1; //UBRR Formula
  UBRR0H = (unsigned char)(ubrr >> 8);
  UBRR0L = (unsigned char)ubrr;
  UCSR0B = (1 << RXEN0) | (1 << TXEN0); 
  UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); 
}

// Transmit a character over UART
void uart_transmit(unsigned char data) 
{
  while (!(UCSR0A & (1 << UDRE0)));
  UDR0 = data;
}

// Receive a character over UART
unsigned char uart_receive(void) 
{
  while (!(UCSR0A & (1 << RXC0)));
  return UDR0;
}

int main() 
{
  uart_init(BaudRate); // UART init 

  unsigned char received_char;
  int eeprom_address = 0;  // EEPROM address counter

  // Receive data and store in EEPROM
  while (1) 
  {
    received_char = uart_receive(); 

    if (eeprom_address >= EEPROM_SIZE) // Check EEPROM
    {  
      memory = true; // If Full make memory flag true
      break;  // Stop receiving data
    }

    eeprom_write_byte((uint8_t *)eeprom_address, received_char); // Write in EEPROM from 0 address
    eeprom_address++;
    if (received_char == '#') // '#' char - for end of message 
    {
    break;  
    }
  }

  // Send Data Back to PC
  eeprom_address = 0; // Reset EEPROM address to start reading
  while (memory == false) // Check for EEPROM Full
  {
    received_char = eeprom_read_byte((uint8_t *)eeprom_address);
    uart_transmit(received_char);
    eeprom_address++;
    if (received_char == '#') // End of message
    { 
    for (uint16_t i = 0; i < eeprom_address; i++) 
    {
      eeprom_write_byte((uint8_t *)i, 0xFF); // Clear memory after sending data - this part is not required since it automatically overwrites when next message is received
    }
    break;
    }
  }


  if(memory == true) // If EEPROM Full - Send '$' for PC to show warning message & then clear EEPROM
  {
  uart_transmit('$');
  for (uint16_t i = 0; i < eeprom_address; i++) 
  {
    eeprom_write_byte((uint8_t *)i, 0xFF); // Clear EEPROM from address 0
  }
  }

  return 0;
}
