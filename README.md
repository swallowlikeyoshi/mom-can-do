# mom-can-do (엄마도 할 수 있다)

회사에서 경리·사무를 하시는 어머니가 ChatGPT 데스크톱 앱(Windows)에서
대화로 따라 하며 배우는 강의 스킬 묶음이에요.

## 설치

ChatGPT 데스크톱 앱에서 권한을 가장 넓은 것(Full access, 한글 화면은 "전체"가 들어간 이름)으로 바꾼 뒤, 아래 문장을 붙여 넣으세요.

```
이 주소의 스킬을 내 컴퓨터에 설치해줘: https://github.com/swallowlikeyoshi/mom-can-do
```

앱을 껐다 켜고 "엄마 강의"라고 입력하면 시작돼요.

## 스킬

| 스킬 | 하는 일 |
|------|---------|
| `mom-class` | 입구. 진도를 보고 이어서 시작, "엄마 강의 업데이트해줘" 처리 |
| `mom-0-start` | 강의 0 준비 운동 (권한, 기밀, 모델, 캡처, 스킬 부르기, 새 채팅) |
| `mom-help` | 막혔을 때 같이 해결하고, 안 되면 아들에게 보낼 요약 만들기 |

강의 1~6은 준비 중이에요.

## 개발

```bash
python3 scripts/check_skills.py --expect mom-class,mom-0-start,mom-help
python3 -m unittest discover tests
```
