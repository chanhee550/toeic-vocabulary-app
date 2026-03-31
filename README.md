# TOEIC 영단어장

TOEIC 시험 대비를 위한 영단어 학습 웹 애플리케이션입니다. 서버 없이 HTML 파일 하나만으로 단어 목록 조회, 타이핑 학습, 테스트까지 모두 가능합니다.

## 주요 기능

- **단어 목록**: 약 2,000개 이상의 TOEIC 필수 영단어를 IPA 발음 기호 및 한국어 뜻과 함께 제공
- **카테고리 분류**: 단어를 `학습완료` / `헷갈림` / `미학습` 3단계로 분류하여 관리
- **타이핑 학습**: 한국어 뜻을 보고 영단어를 직접 타이핑하며 학습 (반복 횟수, 순서 설정 가능)
- **테스트 모드 (2종류)**:
  - **한→영 타이핑 테스트**: 한국어 뜻을 보고 영단어를 직접 입력
  - **영→한 4지선다 테스트**: 영단어를 보고 올바른 한국어 뜻을 선택
- **동의어 감지**: 한→영 테스트에서 정답과 다른 단어를 입력해도 뜻이 유사하면 동의어로 인정
- **TTS 발음 재생**: Web Speech API를 활용한 영단어 원어민 발음 재생
- **사전 조회 및 번역**: Free Dictionary API로 영영 사전 정보 조회, MyMemory API로 한국어 번역 제공
- **다크/라이트 모드**: 사용자 환경에 맞는 테마 전환 지원
- **단어 추가**: 사용자가 직접 새로운 단어를 추가 가능
- **학습 데이터 저장**: localStorage를 활용하여 학습 상태, 설정, 커스텀 단어를 브라우저에 자동 저장
- **PC/모바일 대응**: PC용(`toeic-typing.html`)과 모바일용(`toeic-mobile.html`) 두 가지 버전 제공

## 사용 방법

별도의 설치나 서버가 필요하지 않습니다.

1. **PC 사용자**: `toeic-typing.html` 파일을 웹 브라우저에서 열기
2. **모바일 사용자**: `toeic-mobile.html` 파일을 웹 브라우저에서 열기

> 인터넷 연결은 사전 조회 및 번역 기능 사용 시에만 필요합니다.

## 파일 구조

```
toeic words/
├── toeic-typing.html        # PC용 메인 HTML (단어 데이터 내장)
├── toeic-mobile.html         # 모바일용 메인 HTML (단어 데이터 내장)
├── build_toeic.py            # PC용 HTML 빌드 스크립트 (Python)
├── build_toeic_mobile.py     # 모바일용 HTML 빌드 스크립트 (Python)
├── gen_pronun.py             # IPA → 발음 표기 변환 스크립트
├── toeic_words.json          # 전체 단어 데이터 (word, meaning, ipa, pronun)
├── toeic_data_compact.json   # 압축 단어 데이터
├── toeic_vocab.pdf           # 원본 TOEIC 단어 PDF
├── LICENSE                   # MIT 라이선스
├── README.md                 # 프로젝트 설명서 (이 파일)
└── REPORT.md                 # 개발 보고서
```

## 기술 스택

- **프론트엔드**: 순수 HTML / CSS / JavaScript (프레임워크 없음)
- **사전 API**: [Free Dictionary API](https://dictionaryapi.dev/) (영영 사전)
- **번역 API**: [MyMemory Translation API](https://mymemory.translated.net/) (영→한 번역)
- **음성 합성**: Web Speech API (TTS 발음 재생)
- **데이터 저장**: localStorage (브라우저 내장 저장소)
- **빌드 도구**: Python (JSON 데이터를 HTML에 내장하여 단일 파일 생성)

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.

단어 데이터 출처: [dokjongban.com](https://www.dokjongban.com/voca-book)
단어 데이터의 저작권은 원저작자에게 있으며, 본 프로그램은 학습 목적으로 제작되었습니다.

## 작성자

**김찬희 (Kim Chanhee)**
