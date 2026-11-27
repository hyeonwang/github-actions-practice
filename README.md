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
