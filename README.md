# OrderLab | Python CI/CD 실습

| 단계 | 실습 |
| --- | --- |
| 1 | `subtotal`의 정상·0·음수 입력을 pytest로 검사하고 Ruff를 실행한다. |
| 2 | 할인 적용 후 배송비를 계산한다. 49,999원, 50,000원, 50,001원을 매개변수화하고 할인율 -1%와 101%에서 예외를 확인한다. |
| 3 | CSV 매출을 집계한다. `tmp_path`와 fixture로 각 테스트의 데이터를 준비하고 CI에서 커버리지 XML을 보관한다. |
| 4 | FastAPI의 주문 생성·조회 API를 `TestClient`로 검증한다. CI는 lint와 Ubuntu·Windows 테스트를 병렬 실행한다. |
| 5 | 샘플 CSV로 HTML을 생성한다. `main`의 Push에서 lint와 모든 테스트가 성공하면 GitHub Pages에 배포한다. |

## 실행 방법

Python 3.14에서 프로젝트 루트를 열고 실행한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
ruff check .
ruff format --check .
python -m pytest -q --cov=orderlab --cov-report=term-missing --cov-report=xml
python generate_report.py
```

macOS/Linux에서는 `source .venv/bin/activate`로 가상환경을 켠다. 샘플 보고서는 `site/index.html`에 생성되며 매출은 **35,000 KRW**다.

## Actions에서 확인하기

- `Actions → OrderLab CI-CD`의 실행 상세에 lint, Ubuntu 테스트, Windows 테스트가 표시된다. Artifacts에는 OS별 `coverage-xml-*`이 올라간다.
- PR에서 테스트 기댓값을 20,000에서 20,001로 바꾸면 pytest가 `AssertionError`로 실패한다. 실패한 테스트의 실제값과 기댓값을 비교하고, 기댓값을 복구하여 같은 PR에서 CI가 통과하는지 확인한다.
- 사용하지 않는 import를 추가하면 Ruff의 `F401`이 발생한다. import를 제거하고 `ruff check .`를 다시 실행한다.
- Pages 게시 소스는 `Settings → Pages → Source → GitHub Actions`다. 배포 주소는 성공한 실행의 `github-pages` 환경에서 확인한다.

[실패 재현 실행](https://github.com/hyeonwang/github-actions-practice/actions/runs/46020902468)에서는 Ruff `F401`과 pytest `AssertionError`를 확인할 수 있다. 같은 PR의 다음 커밋에서 import와 기댓값을 복구했다.

## GitHub Actions 예제

[교수님 실습 저장소](https://github.com/DBChoi85/git-practice)의 예제를 `.github/workflows`에 정리했다. Actions에서 `workflow_dispatch` 예제를 골라 **Run workflow**로 실행한다.

- **기본 구조와 오류** — `hello.yml`, `manual.yaml`, `shell.yaml`, `yaml_error.yaml`, `run_time_error.yaml`. [워크플로 문법 오류 예제](practice/workflow_error.yaml)는 `job:`을 `jobs:`로 고치는 연습에 사용한다.
- **컨텍스트와 변수** — `context.yaml`, `env.yaml`, `env_ref.yaml`, `inter_env_ref.yaml`, `val_ref.yaml`, `secret_ref.yaml`. 변수·시크릿은 Actions 설정에서 실습용 값으로 지정할 수 있다. 시크릿 예제는 설정 여부를 출력한다.
- **표현식과 함수** — `literal.yaml`, `operator.yaml`, `object-filter.yaml`, `string-function.yaml`, `string-create.yaml`, `json-function.yaml`, `hash.yaml`.
- **실행 조건과 이름** — `condition.yaml`, `condition-workflow.yaml`, `status-check.yaml`, `job-status.yaml`, `run-name.yaml`. 상태 함수 실습에서는 실패와 건너뜀 자체가 관찰 대상이다.
- **실행 중 값 전달** — `var.yaml`, `job-output.yaml`. 같은 job의 다음 step에는 `GITHUB_ENV`, 다른 job에는 `GITHUB_OUTPUT`과 `needs`를 사용한다.
- **이슈 이벤트** — `issue-comment.yaml`은 새 이슈 이벤트에서 실행한다. `push-issue.yaml`은 `practice/push-issue` 브랜치의 Push에서 실행한다.

## 손코딩 연습

1. 정수 단가와 수량을 받아 소계를 구한다. 음수는 예외로 처리한다. 정상·0·음수 테스트를 각각 쓴다.
2. 할인 후 0원 초과 50,000원 미만에 배송비 3,000원을 더한다. 할인 범위를 검증하고 경계값 세 개를 `parametrize`로 테스트한다.
3. `price,quantity` CSV를 집계하고 `tmp_path`로 정상·빈 파일·잘못된 숫자를 테스트한다.
4. 주문 생성 POST와 조회 GET을 구현한다. 상황별로 201·200·404·422 테스트를 작성한다.
5. Push/PR에서 검사하는 YAML을 쓰고, Ubuntu·Windows 테스트를 병렬화한다. 모든 검사가 성공한 `main` Push에서만 Pages 배포가 실행되도록 한다.
6. 첫 job에서 값을 만들고 둘째 job에서 읽는다. `id`, `GITHUB_OUTPUT`, job outputs, `needs`를 연결한다.
