#include <avr/io.h>
#include "my_atmega128.h"
#include "my_LCD.h"
#include "hepheir.h"

int main(void) {
    int i;
    int key;

    // 입출력 설정
    DDRC = DDRC | 0b11111100; // LED : 출력
    KEYMAT_initialize();

    while (1) {
        key = waitKey(0);

        // 5번 키가 눌렸을 때
        switch(key) {
            case 9: // 5번 키
                for (i = 7; i >= 2; i--) {
                    PORTC |= 1 << i;
                    Delay_ms(160);
                    LED_turn_off_all();
                }
                break;

            case 13: // 8번 키
                for (i = 2; i <= 7; i++) {
                    PORTC |= 1 << i;
                    Delay_ms(160);
                    LED_turn_off_all();
                }
                break;
            
            default:
                break;
        }
        LED_turn_off_all();
    }
}
