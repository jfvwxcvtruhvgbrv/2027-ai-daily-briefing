# AI 데일리 — 매일 아침 글로벌 AI 일간 브리핑

매일 아침 7시 전후(KST) 전세계 AI 생태계 소식을 일간지 형식으로 정리해
**메일(요약 + 1면 사진)** 과 **웹 보고서(GitHub Pages, 사진·차트·심층 리포트)** 로 받는다.

## 동작 방식
```
[Claude 예약 작업 — Claude Pro 구독 사용량, API 비용 없음]
  KAIST SketchLab Daily AI 새 항목 → 원문 추적 심층 리서치
  + 글로벌·국내 AI 뉴스 취재 → 교차 검증(✅ ☑️ ⚠️) → 기사·1면·해설 작성
  → issues/YYYY-MM-DD.json push   (지침: prompts/daily_task.md)
        ↓ push 트리거
[GitHub Actions — 무료]  .github/workflows/publish.yml
  공식 페이지 대표 이미지 확인 → 일간지형 보고서 → GitHub Pages
  → Gmail SMTP로 그날 호 메일 발송
```

| 경로 | 역할 |
|---|---|
| `issues/` | 날짜별 호 (JSON) |
| `schema/ISSUE_SCHEMA.md` | 호 JSON 형식 |
| `prompts/daily_task.md` | 매일 예약 작업이 따르는 취재·편집 지침 |
| `state.json` | SketchLab 마지막 처리 번호, 최근 다룬 사건 |
| `render/` | 검증·이미지·보고서/메일 템플릿·발송 |
| `examples/` | 렌더링 테스트용 샘플 |

## 처음 한 번 설정
1. **Claude GitHub 앱 권한**: https://github.com/apps/claude/installations/select_target 에서 이 저장소 추가 (예약 작업이 push하려면 필요)
2. **GitHub Pages**: Settings → Pages → Build and deployment → Source를 **GitHub Actions**로
3. **Gmail 앱 비밀번호**: Google 계정 → 보안 → 2단계 인증 켜기 → "앱 비밀번호"에서 16자리 발급
4. **Secrets** (Settings → Secrets and variables → Actions → New repository secret)
   - `GMAIL_ADDRESS`: 보내는 Gmail 주소
   - `GMAIL_APP_PASSWORD`: 위 16자리 앱 비밀번호
   - `MAIL_TO`: 받는 주소 (여러 명은 쉼표로)

## 수동 실행
- Actions → "AI 데일리 발행" → Run workflow → 날짜 입력: 그 호를 다시 빌드하고 메일 재발송
- 로컬 확인: `python3 -m render.build --issues examples --no-images --email 2026-11-07` → `site/`, `out/`

## 실패하면
- 호 JSON 형식 오류, 메일 Secret 누락, SMTP 실패 → Actions가 실패로 끝나고 GitHub 실패 알림 메일이 옴
- 공식 이미지를 못 찾으면 사진만 빠지고 계속 진행 (로그에 `[WARN] 이미지`)
- 예약 작업이 실패하면 push가 없어 그날 메일이 오지 않음 (예약 작업 실패 알림 확인)

## 원칙
- 원문 복사 금지, 직접 재작성 요약 + 원문 링크
- 사진은 기업 공식 페이지 대표 이미지만 원본 주소로 싣고 출처 표기, 인물·보도사진 제외, 저장소에 복사하지 않음
- SketchLab은 목록 페이지만 읽고 좋아요 집계 링크(`/go/`)는 호출하지 않음
- X·LinkedIn은 공개 웹 검색으로 확인된 포스트만
- 투자 판단의 근거가 아님
