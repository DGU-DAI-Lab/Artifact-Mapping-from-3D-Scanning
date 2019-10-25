#include <avr/io.h>

#include <stdio.h>
#include "my_atmega128.h"
#include "my_LCD.h"
#include "hepheir.h"

int main(void) {
    int key;
    int ADC_enable = 0;
    double voltage;
    char text[16];

    // 입출력 설정
    DDRC |= 0b11111100; // LED : 출력
    DDRF &= ~(0b00000011); // ADC_0~1 을 입력으로 

    ADMUX = 0x00; // VR1 사용
    ADCSRA = 0xF7;
    // AD converter 활성화, 변환동작 시작, Free running mode,
    // 인터럽트 사용안함, ADC 클럭을 128분주	

    LCD_enable();
    KEYMAT_enable();

    LCD_initialize();
    Delay_ms(5);

    while (1) {       
        // 키 메트릭스의 각 버튼별로 기능 할당. 
        key = waitKey(0);
        switch(key) {
            case 3: // KEY_F1 (S3)
                // AD convert 동작 시작
                ADC_enable = 1;
                PORTC |= 0x04;
                break;

            case 4: // KEY_1 (S4)
                // AD convert 동작 정지
                ADC_enable = 0;
                PORTC &= ~(0x04);
                break;
        }

        if (ADC_enable) {
            // AD conversion이 완료되기까지 대기. (폴링 방식)
            while(!(ADCSRA & 0x10)); // busy waiting

            voltage = (double) 5 *  ADC / 0b1111111111;
            sprintf(text, "%5.2f[V]        ", voltage);
            LCD_string(0x80, text);

            // AD conversion의 완료를 나타내는 비트를 clear.
            ADCSRA |= 0x10;
        } else {
            LCD_string(0x80, "Eh?...          ");
        }
    }
}
