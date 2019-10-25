void LCD_command(unsigned char command)  /* write a command(instruction) to text LCD */
{                                        
    PORTC &= ~(1<<1 | 1<<0); 		// E = 0, Rs = 0  
    PORTA  = command;		// output command
    PORTC |= 1<<1;  			// E = 1
    asm (" PUSH  R0 ");			// delay for about 250 ns
    asm (" POP   R0 ");
    PORTC &= ~1<<1; 			// E = 0
    Delay_us(50);
}

void LCD_data(unsigned char data)		/* display a character on text LCD */
{
    PORTC &= ~1<<1; 			// E = 0, Rs = 1 
    PORTC |= 1<<0; 
    PORTA = data;			// output data
    PORTC |= 1<<1; 			// E = 1
    asm (" PUSH  R0 ");			// delay for about 250 ns
    asm (" POP   R0 ");
    PORTC &= ~1<<1; 			// E = 0
    Delay_us(50);
}

void LCD_string(char command, char *string)   /* display a string on LCD */
{
    LCD_command(command);			// start position of string
    while(*string != '\0') {			// display string
        LCD_data(*string);
        string++;
    }
}

void LCD_initialize(void)			/* initialize text LCD module */
{
    PORTC |= 1<<1;				// E = 1, Rs = 1 (dummy write)    
    PORTC |= 1<<0;
    PORTC &= ~1<<1;				// E = 0, Rs = 1
    PORTC |= 1<<0;
    Delay_ms(2);

    LCD_command(0x38);	       // function set(8 bit, 2 line, 5x7 dot)
    LCD_command(0x0C);	       // display control(display ON, cursor OFF)
    LCD_command(0x06);	       // entry mode set(increment, not shift)
    LCD_command(0x01);	       // clear display
    Delay_ms(2);
}