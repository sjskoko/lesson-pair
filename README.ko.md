# LessonPair

**영상 예습과 수업 후 복습을 하나의 흐름으로 연결하는 오픈소스 스킬입니다.**

[English](README.md) · [사용법](docs/usage.md) · [가상 예시](examples/README.md)

영상 하나를 공부하고 선생님과 대화한 뒤, 작문과 피드백을 두 페이지로 연결합니다.

| ① 영상 예습 자료 | ② 수업·복습 기록 |
| --- | --- |
| 영상·제공된 자막·구간별 해석 | 직접 쓴 작문 원본·선생님 메모 |
| 표현과 문법 메모 | 문장별 교정·정확한 문법 설명 |
| 수업에서 사용할 표현 3개 | 정답을 가린 문제·재작문 |

원본은 보존하고, 선생님 피드백과 AI 보완을 구분합니다. 기존 수업은 이어서 수정하며, 미완성 문장의 의미나 점수·복습 완료 여부를 임의로 채우지 않습니다. 노션의 수업 목록·복습 대기·달력·양식 보기를 활용하도록 안내합니다.

## 바로 실행하기

Python 3.10 이상에서 실행합니다. 추가 패키지와 API 키가 필요하지 않습니다.

```bash
git clone https://github.com/sjskoko/lesson-pair.git
cd lesson-pair
python3 skills/lesson-pair/scripts/lesson_pair.py render examples/lesson.synthetic.json --out output/demo
python3 skills/lesson-pair/scripts/lesson_pair.py check output/demo/02-review.notion.md
```

이 명령은 가상 자료를 로컬 초안으로 정리합니다. AI 교정이나 노션 저장은 실행하지 않습니다. 노션용 Markdown은 연결 도구를 통한 작성용이며, 일반 편집기에 붙여 넣으면 그대로 표시될 수 있습니다.

## GPT·Codex에서 사용하기

스킬 설치를 지원하는 환경에서 다음 폴더를 설치합니다.

`https://github.com/sjskoko/lesson-pair/tree/main/skills/lesson-pair`

설치 후 `@lesson-pair` 또는 호스트에서 지원하는 `$lesson-pair`로 호출합니다.

> 이 수업을 LessonPair로 정리해줘. 기존 영상 예습 자료와 연결하고, 내 작문 원본·선생님 메모를 보존해줘. 교정과 복습 문제도 추가해줘.

공개 저장소를 읽는 데 별도의 GitHub 접근 토큰은 필요하지 않습니다. 다만 **AI가 교정·정리할 때는 모델 토큰과 이용 한도가 적용**되며, 개인 노션에 저장하려면 노션 연결 권한이 필요합니다. 일반 커스텀 GPT가 이 저장소를 자동 설치하는 것은 아닙니다. 자세한 적용 방법은 [사용 가이드](docs/usage.md)에 있습니다.

## 개인정보

실제 학습 기록·연락처·개인 노션 주소는 포함하지 않습니다. 모든 예시는 새로 만든 가상 자료입니다. 자신의 학습 기록은 공개 저장소에 올리지 마세요.

유용했다면 Star로 알려주세요. 개선 제안과 다른 언어 예시는 [기여 안내](CONTRIBUTING.md)에 따라 공유할 수 있습니다.
