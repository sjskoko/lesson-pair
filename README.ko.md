# LessonPair — 좋아하는 영상을, 내 영어로 설명하기

**영상 하나를 고르고, 짧게 대화하고, 내가 쓴 두 답변을 비교하세요.**

영어 원문 영상에서 시작하는 오픈소스 영어 학습 스킬과 ChatGPT/Codex 플러그인입니다. 처음 말하지 못한 표현을 중심으로 연습한 뒤, 직접 다시 설명하도록 안내합니다.

[웹사이트·예시](https://sjskoko.github.io/lesson-pair/ko/) · [설치 가이드](https://sjskoko.github.io/lesson-pair/ko/guide/) · [English](README.md) · [레거시](docs/legacy.md)

## 사용자는 세 가지만 합니다

1. **영상 선택:** 영어 영상 링크를 줍니다. 접근 가능한 자막을 사용하며, 가져올 수 없다면 자막이나 짧은 발췌를 붙여 넣습니다.
2. **짧은 대화:** 먼저 영어 1–3문장으로 설명합니다. AI는 막힌 표현 한두 개를 골라 한 번에 질문 하나씩 연습시킵니다.
3. **내 답변 비교:** 예시를 보지 않고 다시 설명합니다. 첫 답변과 재도전 답변을 비교하고, 나중에 다른 맥락에서 떠올려 봅니다.

선생님과 노션은 선택 사항입니다. 초보자는 짧은 문장부터 시작하고, 필요할 때 힌트와 예시를 받습니다. 60초 설명은 선택 목표입니다.

## AI가 고친 문장과 내 실력을 구분합니다

| 첫 시도 | 집중 연습 | 재도전 |
| --- | --- | --- |
| Trees makes shade. Roots need place. | provide shade, room to grow | Trees provide shade. Their roots need room to grow. |

위 내용은 **가상 데모**입니다. 실제 학습에서는 두 답변 모두 사용자가 작성합니다. AI가 대신 쓴 문장을 학습 성과로 표시하지 않고, 도움을 받은 답변은 그렇게 기록합니다. 이 프로그램의 학습 효과를 실험으로 입증했다는 뜻도 아닙니다.

## 내 AI로 시작하기

- **ChatGPT/Codex:** 지원되는 저장소 마켓플레이스나 워크스페이스 경로로 스킬형 플러그인을 설치합니다. 현재 호스트의 AI를 사용하므로 별도 API 키가 필요하지 않습니다. [상세 안내](docs/plugin.md)
- **다른 AI·커스텀 GPT:** `SKILL.md`, `guided-session.md`, `source-access.md`를 첨부해 수동으로 사용합니다. 네이티브 플러그인 설치와는 다릅니다.
- **내 모델·API:** Python 로컬 도구에 OpenAI 호환 엔드포인트를 설정합니다. 로컬 Ollama 서버도 같은 API 형식으로 연결할 수 있습니다. [설정 안내](skills/lesson-pair/references/own-ai.md)

스킬을 불러온 뒤 이렇게 시작하세요:

> LessonPair로 이 영어 영상을 내 말로 설명하도록 도와줘: [링크]. 자막을 가져올 수 없으면 내게 발췌를 요청해. 한 번에 작은 질문 하나씩 하고, 내가 답하기 전에 모범 답안을 먼저 보여주지 마. 설명은 한국어로 해 줘.

Codex 저장소 마켓플레이스 추가:

```bash
codex plugin marketplace add sjskoko/lesson-pair --ref main
```

추가 후 지원되는 플러그인 화면에서 `lesson-pair`를 설치합니다. **공개 OpenAI 플러그인 디렉터리에 등록된 상태는 아닙니다.** ChatGPT의 설치 경로와 사용 가능 여부는 클라이언트·워크스페이스에 따라 달라집니다.

## 로컬 실행 예시

Python 3.10 이상과 별도로 실행한 모델 서버가 필요합니다.

```bash
git clone https://github.com/sjskoko/lesson-pair.git
cd lesson-pair
export LESSONPAIR_BASE_URL='http://localhost:11434/v1'
export LESSONPAIR_MODEL='YOUR-INSTALLED-MODEL'
python skills/lesson-pair/scripts/learn.py start --source examples/transcript.synthetic.txt --language Korean
python skills/lesson-pair/scripts/learn.py run
python skills/lesson-pair/scripts/learn.py export
```

원격 API는 HTTPS 주소와 모델을 설정하고, 필요한 키는 환경변수 `LESSONPAIR_API_KEY`로만 전달합니다. 채팅·웹페이지·공개 저장소에 키를 넣지 마세요. HTTP 연동은 로컬 모의 서버로 검증하며, 실제 모델별 동작과 수업 품질은 별도 확인이 필요합니다.

선택적으로 `yt-dlp`를 설치하면 `start --url YOUTUBE_URL`로 영어 자막을 시도합니다. 자동 음성 전사 기능은 아니며, 자막이 없거나 접근이 막히면 파일을 제공해야 합니다. `/hint`, `/example`, `/quit`를 사용할 수 있고, API 오류 후에도 답변이 저장되어 이어서 진행할 수 있습니다.

## 기록·비용·레거시

기록은 기본적으로 Git에서 제외된 `private/`에 저장됩니다. AI 사용 시에는 원문과 답변이 선택한 제공자에게 전달됩니다. 노션 연결은 선택 사항이며 기존 예습·수업 기록 쌍 구조와 표 복구 기능은 유지합니다.

코드는 MIT 라이선스로 무료입니다. **AI 실행에는 토큰·연산·호스트 이용 한도가 적용됩니다.** 발음 평가, 자동 알림, 학습 효과 보장은 제공하지 않습니다. 공개 예시는 모두 새로 만든 가상 자료이며 실제 학습 기록과 개인정보는 포함하지 않습니다.

이전 버전은 [`legacy/english`](https://github.com/sjskoko/lesson-pair/tree/legacy/english)에 보존했습니다. 기존 JSON 포맷과 오프라인 정리 도구도 계속 사용할 수 있습니다. [변경 내역](CHANGELOG.md)

유용하다면 GitHub Star로 다시 찾아오세요. 피드백에는 실제 개인 기록 대신 가상 예시를 사용해 주세요.
