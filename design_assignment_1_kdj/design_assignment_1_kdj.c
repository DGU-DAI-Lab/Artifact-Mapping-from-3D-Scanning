#include <avr/io.h>
#include "my_atmega128.h"

void LED_turn_off_all();

void KEY_SCAN_reset();
void KEY_SCAN_set(int n);
int  KEY_DATA_get(int n);

int main(void) {
    int i;

    // 입출력 설정
    DDRC = DDRC | 0b11111100; // LED : 출력
    DDRD = DDRD & 0b00001111; // KEY_DATA_0~3 : PD4~7 : 입력
    DDRE = DDRE | 0b11110000; // KEY_SCAN_0~3 : PE4~7 : 출력

    while (1) {
        // 5번 키가 눌렸을 때
        KEY_SCAN_reset();
        KEY_SCAN_set(1);
        if (KEY_DATA_get(2)) { 
            for (i = 7; i >= 2; i--) {
                PORTC |= 1 << i;
                Delay_ms(160);
                LED_turn_off_all();
            }
        }
        else LED_turn_off_all();

        // 8번 키가 눌렸을 때
        KEY_SCAN_reset();
        KEY_SCAN_set(2);
        if (KEY_DATA_get(2)) {
            for (i = 2; i <= 7; i++) {
                PORTC |= 1 << i;
                Delay_ms(160);
                LED_turn_off_all();
            }
        }
        else LED_turn_off_all();
    }
}

void LED_turn_off_all() {
    // 모든 LED를 OFF.
    PORTC = PORTC & 0x03;
}

void KEY_SCAN_reset() {
    // 모든 KEY_SCAN 핀의 출력을 0으로.
    PORTE &= 0x0F;
}

void KEY_SCAN_set(int n) {
    // KEY_SCAN 의 n번 핀의 출력을 1로.
    PORTE |= 1 << (n + 4);
}

int KEY_DATA_get(int n) {
    // KEY_DATA 의 n번 핀의 입력을 반환.
    return PIND & 1 << (n + 4);
}