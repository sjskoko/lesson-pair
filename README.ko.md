# LessonPair — 좋아하는 영상을 내 영어로 설명하기

**영상은 이해했는데, 영어로 설명하려면 말이 막히나요?**

영어 영상 하나로 내 AI와 짧게 연습하고, **내가 직접 쓴 첫 답변과 다음 답변**을 비교하는 오픈소스 영어 학습 도구입니다.

**[가상 데모 보기](https://sjskoko.github.io/lesson-pair/ko/#demo)** · [설치 가이드](https://sjskoko.github.io/lesson-pair/ko/guide/) · [플러그인](docs/plugin.md) · [English](README.md)

## 사용자는 세 가지만 하면 됩니다

1. **관심 있는 영상 고르기.** 접근 가능한 영어 자막을 사용하고, 없으면 자막이나 짧은 발췌문을 넣습니다.
2. **AI와 짧게 대화하기.** 먼저 설명해 보고, 막힌 표현을 한 질문씩 연습합니다.
3. **내 답변 비교하기.** 예시를 보지 않고 다시 설명한 뒤, 처음 답변과 달라진 부분을 확인합니다.

혼자 시작할 수 있고 선생님이나 노션은 필수가 아닙니다. 처음에는 1~3문장으로 충분합니다. 60초 설명은 선택 목표입니다.

## AI가 대신 잘 쓴 문장을 내 실력으로 표시하지 않습니다

가상의 첫 답변 “Trees makes shade. Roots need place.”에서 표현을 연습한 뒤, 사용자가 직접 다시 답합니다. AI 교정, 원문, 재답변, 도움 여부를 따로 기록합니다. 재답변을 하지 않으면 빈 상태로 남깁니다. 공개 예시는 모두 새로 만든 가상 자료이며 실제 개인 기록이나 학습 효과 증거가 아닙니다.

## 내 AI로 사용하기

| 방법 | 실행 방식 |
| --- | --- |
| ChatGPT / Codex 플러그인 | 지원되는 호스트에 설치하고 현재 사용하는 AI로 학습 |
| 다른 AI | 스킬을 설치하거나 안내 파일을 첨부해 수동 사용 |
| 내 API / 로컬 모델 | OpenAI 호환 Chat Completions 서버에 Python 도구 연결 |
| 노트만 정리 | 오프라인 Markdown 내보내기와 기존 노션 포맷터 |

플러그인 패키지와 저장소 마켓플레이스를 제공합니다. 호스트의 설치 지원 및 관리자 정책이 적용되며, 공개 플러그인 디렉터리에 심사·등록된 상태는 아닙니다. [설치 절차](docs/plugin.md).

로컬 모델 예시:

```bash
export LESSONPAIR_BASE_URL='http://localhost:11434/v1'
export LESSONPAIR_MODEL='YOUR-INSTALLED-MODEL'
python skills/lesson-pair/scripts/learn.py start --source examples/video.synthetic.txt --language Korean
python skills/lesson-pair/scripts/learn.py run
python skills/lesson-pair/scripts/learn.py export
```

모델 서버와 모델은 별도로 준비합니다. 외부 API 키는 환경변수로만 전달합니다. `/hint`, `/example`, `/quit` 명령을 지원하고 중단한 학습은 같은 `run` 명령으로 이어갑니다. [상세 설정](skills/lesson-pair/references/own-ai.md).

영상 URL은 선택 설치하는 yt-dlp로 영어 자막을 가져올 수 있을 때 사용합니다. 모든 영상 접근이나 자동 음성 인식을 보장하지 않습니다. 자막이 없으면 파일을 요청합니다.

## 비용과 개인정보

코드·스킬은 MIT 라이선스입니다. AI 사용에는 토큰 및 서비스별 요금·한도가 적용됩니다. `run`은 자막과 답변을 내가 지정한 AI에 전송합니다. 로컬 기록은 기본적으로 `private/`에 저장하고 Git에서 제외합니다. 웹사이트에서 API 키를 입력받지 않습니다. 공개 이슈에 실제 학습 기록을 올리지 마세요.

회상과 재시도에 기반한 설계지만 이 제품의 학습 효과가 실험으로 검증된 것은 아닙니다. 텍스트만으로 발음이나 유창성을 평가하지 않습니다. 복습 제안은 자동 알림이 아닙니다.

## 기존 버전도 보존합니다

기존 수업·노션 중심 버전은 [`legacy/english`](https://github.com/sjskoko/lesson-pair/tree/legacy/english)에 보존했습니다. 기존 JSON 포맷터도 유지하며 개인 노션 페이지를 자동 변경하지 않습니다.

한 영상으로 시작해 보세요. 도움이 되었다면 **GitHub Star**로 저장하고, 가상 예시로 개선점을 제안해 주세요. [기여 안내](CONTRIBUTING.md).
