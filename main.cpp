
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
  DDRB |= (1 << PB5); // LED Notification config

  uart_init(BaudRate); // UART init 

  unsigned char received_char;
  int eeprom_address = 0;  // EEPROM address counter

  // Receive data from PC and store in EEPROM
  while (1) 
  {
    received_char = uart_receive(); 
    eeprom_write_byte((uint8_t *)eeprom_address, received_char); // Write in EEPROM from 0 address
    eeprom_address++;
    if (received_char == '#') // '#' char - for end of message 
    {
    PORTB |= (1 << PB5); // Turn Led 13 ON for Message Received Notification
    break;  
    }
  }

  return 0;
}
