/*
2018~2019 Coded by hepheir@gmail.com
EICE. Sophomore 2018212236 Kim Dong Joo
*/
void LED_turn_off_all() {
    PORTC = PORTC & 0x03;
}


void KEYMAT_enable() {
    DDRD = DDRD & 0b00001111; // KEY_DATA_0~3 --> PD4~7 에 대응 : 입력으로 설정
    DDRE = DDRE | 0b11110000; // KEY_SCAN_0~3 --> PE4~7 에 대응 : 출력으로 설정
    
    PORTE &= 0x0F; // KEY_SCAN 모든 핀을 리셋
}

void LCD_enable() {
    DDRA  = 0xFF;
    PORTA = 0x00;
}

int waitKey(int time_ms) {
    /* 
    현재 눌린 키 메트릭스 버튼의 소자번호 (S+숫자)의 숫자를 반환하는 함수.
    아무 버튼도 눌려있지 않으면 `0`(false)을 반환한다.
    
    사용하기 전 최소 1회 이상 `KEYMAT_initialize()` 를 실행해 주어야 함.
    */
    int key_scan, key_data;
    int key_S_index;

    key_S_index = 0;

    for (key_scan = 0; key_scan < 4; key_scan++)
    {
        PORTE |= 1 << (key_scan + 4);
        Delay_ms(5);
        for (key_data = 0; key_data < 4; key_data++)
        {
            if (PIND & 1 << (key_data + 4))
            {
                // KEY_MATRIX의 소자번호는 S3번 부터 시작함.
                key_S_index = (4 * key_scan + key_data) + 3;
            }
        }
        PORTE &= ~(1 << (key_scan + 4));
    }
    return key_S_index;
}