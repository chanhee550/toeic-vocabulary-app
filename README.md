# TOEIC 영단어장

TOEIC 시험 대비를 위한 영단어 학습 웹 애플리케이션입니다. 서버 없이 HTML 파일 하나만으로 단어 목록 조회, 타이핑 학습, 테스트까지 모두 가능합니다.

## 배포 링크

- **통합 버전 (자동 기기 감지)**: https://chanhee550.github.io/toeic-vocabulary-app/toeic-unified.html
- **PC 전용**: https://chanhee550.github.io/toeic-vocabulary-app/toeic-typing.html
- **모바일 전용**: https://chanhee550.github.io/toeic-vocabulary-app/toeic-mobile.html

## 주요 기능

- **단어 목록**: 약 2,000개 이상의 TOEIC 필수 영단어를 IPA 발음 기호 및 한국어 뜻과 함께 제공
- **카테고리 분류**: 단어를 `학습완료` / `헷갈림` / `미학습` 3단계로 분류하여 관리
- **북마크**: 단어별 ★ 북마크 기능 및 북마크 카테고리 필터
- **스와이프 상태 전환 (모바일)**: 단어 카드를 좌/우로 스와이프하여 학습 상태 변경 (드래그 거리에 따른 색상 그라데이션)
- **타이핑 학습**: 한국어 뜻을 보고 영단어를 직접 타이핑하며 학습 (반복 횟수, 순서 설정 가능)
- **테스트 모드 (2종류)**:
  - **한→영 타이핑 테스트**: 한국어 뜻을 보고 영단어를 직접 입력
  - **영→한 4지선다 테스트**: 영단어를 보고 올바른 한국어 뜻을 선택
- **동의어 감지**: 한→영 테스트에서 정답과 다른 단어를 입력해도 뜻이 유사하면 동의어로 인정
- **TTS 발음 재생**: Web Speech API를 활용한 영단어 발음 재생 (재생 중 아이콘 전환)
- **사전 조회 및 번역**: Free Dictionary API로 영영 사전 정보 조회, MyMemory API로 한국어 번역 제공
- **다크/라이트 모드**: 사용자 환경에 맞는 테마 전환 지원
- **단어 추가**: 사용자가 직접 새로운 단어를 추가 가능
- **홈 이동**: 타이틀("TOEIC 단어장") 클릭 시 초기 화면으로 이동
- **학습 데이터 저장**: localStorage를 활용하여 학습 상태, 북마크, 설정, 커스텀 단어를 브라우저에 자동 저장
- **PC/모바일 대응**: PC용, 모바일용, 통합(자동 감지) 세 가지 버전 제공

## 사용 방법

별도의 설치나 서버가 필요하지 않습니다.

1. **통합 버전 (권장)**: `toeic-unified.html` — 기기를 자동 감지하여 PC/모바일 버전 표시
2. **PC 사용자**: `toeic-typing.html` 파일을 웹 브라우저에서 열기
3. **모바일 사용자**: `toeic-mobile.html` 파일을 웹 브라우저에서 열기

> 인터넷 연결은 사전 조회 및 번역 기능 사용 시에만 필요합니다.

## 파일 구조

```
toeic-vocabulary-app/
├── index.html                # 진입점 (기기 감지 후 리다이렉트)
├── toeic-typing.html         # PC용 메인 HTML (단어 데이터 내장)
├── toeic-mobile.html         # 모바일용 메인 HTML (단어 데이터 내장)
├── toeic-unified.html        # 통합 버전 (자동 기기 감지)
├── toeic-ios.html            # iOS 전용 HTML
├── toeic_words.json          # 전체 단어 데이터 (word, meaning, ipa, pronun)
├── build_toeic.py            # PC용 HTML 빌드 스크립트
├── build_toeic_mobile.py     # 모바일용 HTML 빌드 스크립트
├── build_unified.py          # 통합 버전 빌드 스크립트
├── build_ios.py              # iOS 버전 빌드 스크립트
├── gen_pronun.py             # IPA → 발음 표기 변환 스크립트
├── report_to_pdf.py          # 보고서 PDF 변환 스크립트
├── REPORT.md                 # 개발 보고서
├── REPORT.html               # 보고서 HTML 버전
├── LICENSE                   # MIT 라이선스
└── README.md                 # 프로젝트 설명서 (이 파일)
```

## 업데이트 내역

### 2026-04-01

**새 기능**
- 모바일 스와이프 상태 전환: 탭 방식에서 스와이프 방식으로 변경 (오른쪽=학습완료, 왼쪽=헷갈림)
- 드래그 거리에 비례한 배경색 그라데이션 효과
- 이미 분류된 단어를 아무 방향으로 스와이프하면 초기화
- 북마크 기능: 단어별 ★ 버튼 + 북마크 카테고리 필터 (모바일/PC)
- 타이틀 클릭 시 초기 화면으로 이동 (모바일/PC)
- 발음 재생 중 ▶→◼ 아이콘 전환, 재생 완료 시 복원

**UI 개선**
- 상단 버튼(추가/Dark) 크기 통일 (min-width)
- 통계 칩과 필터 버튼 시각적 구분 (통계: 배경/테두리 제거)
- 클릭/스와이프 안내 텍스트를 별도 줄로 분리 + 색상으로 구분

**버그 수정**
- 통합 빌드 시 `</script>` 이스케이프 문제 수정 (문자열 분할 방식)
- 모바일 TTS 재생 안 되는 버그 수정 (iOS Safari 호환성)
- 재생 중 아이콘(일시정지) 모바일 렌더링 문제 수정
- 스와이프 핸들러가 북마크/재생 버튼 터치를 가로채는 문제 수정
- 캐시 방지 메타태그 추가 (구버전 표시 문제 방지)

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
