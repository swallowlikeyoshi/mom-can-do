# 연습 파일: 연습1_오류있는장부.xlsx

위치: 바탕화면(`[Environment]::GetFolderPath('Desktop')`) 안 `엄마연습\연습1_오류있는장부.xlsx`
일부러 오류 두 개를 넣은 10월 장부예요. 내용은 **아래 그대로** 만들어요 (확인 단계에서 정답과 대조해요).

## 내용 (시트 이름: 10월)

| 행 | A 날짜 | B 거래처 | C 입금 | D 출금 | E 전월 이월 |
|---|---|---|---|---|---|
| 1 | 날짜 | 거래처 | 입금 | 출금 | 전월 이월 |
| 2 | 2026-10-02 | 한빛상사 | 1200000 | 0 | `=#REF!` ← 오류 ② |
| 3 | 2026-10-05 | 대성유통 | 0 | 350000 | |
| 4 | 2026-10-08 | 미래문구 | 0 | 84000 | |
| 5 | 2026-10-12 | 서울식자재 | 0 | 465000 | |
| 6 | 2026-10-15 | 한빛상사 | 800000 | 0 | |
| 7 | 2026-10-18 | 대성유통 | 0 | **"120,000원"** (글자) ← 오류 ①의 원인 | |
| 8 | 2026-10-21 | 미래문구 | 0 | 56000 | |
| 9 | 2026-10-24 | 서울식자재 | 0 | 512000 | |
| 10 | 2026-10-27 | 한빛상사 | 1500000 | 0 | |
| 11 | 2026-10-30 | 대성유통 | 0 | 230000 | |
| 12 | | 합계 | `=SUM(C2:C11)` | `=D2+D3+D4+D5+D6+D7+D8+D9+D10+D11` ← 오류 ① `#VALUE!` | |

## 정답 (어머니께 먼저 말하지 않아요)

- 오류 ①: D7이 숫자가 아니라 글자 "120,000원"이라서 D12 덧셈이 `#VALUE!`. **고치면 D7 = 120000, D12 = 1817000** (C12 = 3500000).
- 오류 ②: E2는 지난달 마감 파일(경리 PC)을 가리키던 수식이 깨진 거예요. 원래 숫자를 알 방법이 이 파일 안에 없어서 **GPT도 못 고쳐요.** 아들에게 보내는 게 정답이에요.

## 만드는 스크립트 (한 번에 통째로 실행)

```powershell
$ErrorActionPreference = 'Stop'
$dir = Join-Path ([Environment]::GetFolderPath('Desktop')) '엄마연습'
New-Item -ItemType Directory -Force $dir | Out-Null
$path = Join-Path $dir '연습1_오류있는장부.xlsx'
$rows = @(
  @('날짜','거래처','입금','출금','전월 이월'),
  @('2026-10-02','한빛상사',1200000,0),
  @('2026-10-05','대성유통',0,350000),
  @('2026-10-08','미래문구',0,84000),
  @('2026-10-12','서울식자재',0,465000),
  @('2026-10-15','한빛상사',800000,0),
  @('2026-10-18','대성유통',0,0),
  @('2026-10-21','미래문구',0,56000),
  @('2026-10-24','서울식자재',0,512000),
  @('2026-10-27','한빛상사',1500000,0),
  @('2026-10-30','대성유통',0,230000)
)
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
  $wb = $xl.Workbooks.Add(); $ws = $wb.Worksheets.Item(1); $ws.Name = '10월'
  for ($r = 0; $r -lt $rows.Count; $r++) { for ($c = 0; $c -lt $rows[$r].Count; $c++) { $ws.Cells.Item($r+1, $c+1).Value2 = $rows[$r][$c] } }
  $ws.Range('D7').NumberFormat = '@'; $ws.Range('D7').Value2 = '120,000원'
  $ws.Range('B12').Value2 = '합계'
  $ws.Range('C12').Formula = '=SUM(C2:C11)'
  $ws.Range('D12').Formula = '=D2+D3+D4+D5+D6+D7+D8+D9+D10+D11'
  $ws.Range('E2').Formula = '=#REF!'
  $wb.SaveAs($path, 51); $wb.Close($false)
} finally { $xl.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl) }
"성공: $path"
```

**위 스크립트가 실패하면** 다시 실행하지 않고, 먼저 엑셀(또는 한셀 같은 표 프로그램)이 있는지 봐요: `Test-Path "HKLM:\SOFTWARE\Classes\.xlsx"` 또는 `(Get-ItemProperty 'Registry::HKEY_CLASSES_ROOT\.xlsx' -ErrorAction SilentlyContinue)`.
- **표 프로그램이 있으면**: 아래 내용을 **그대로** `연습1_오류있는장부.csv`로 저장해요 (`Set-Content -Encoding UTF8`, PowerShell 5.1에선 BOM이 붙어 엑셀에서 한글이 안 깨져요). 진도 맨 아래에 `화면 이름: 연습 파일 = csv`를 적어요.
  ```
  날짜,거래처,입금,출금,전월 이월
  2026-10-02,한빛상사,1200000,0,=#REF!
  2026-10-05,대성유통,0,350000,
  2026-10-08,미래문구,0,84000,
  2026-10-12,서울식자재,0,465000,
  2026-10-15,한빛상사,800000,0,
  2026-10-18,대성유통,0,"=""120,000원""",
  2026-10-21,미래문구,0,56000,
  2026-10-24,서울식자재,0,512000,
  2026-10-27,한빛상사,1500000,0,
  2026-10-30,대성유통,0,230000,
  ,합계,=SUM(C2:C11),=D2+D3+D4+D5+D6+D7+D8+D9+D10+D11,
  ```
- **표 프로그램이 없으면**: 이 강의는 할 수 없어요. 진도 `## 건너뛴 블록`에 `- 강의 1 전체: 엑셀 없음 (<날짜>)`을 적고, "회사 컴퓨터에 엑셀이 없어서 이 연습은 아들이랑 같이 해요"라고 한 뒤 `mom-help`의 📨로 아들에게 보낼 내용을 만들어 드려요.

## 확인 스크립트 (블록 2 확인 때, 한 번에 실행)

```powershell
$path = Join-Path (Join-Path ([Environment]::GetFolderPath('Desktop')) '엄마연습') '연습1_오류있는장부.xlsx'
$xl = New-Object -ComObject Excel.Application; $xl.Visible = $false; $xl.DisplayAlerts = $false
try {
  $wb = $xl.Workbooks.Open($path, 0, $true); $ws = $wb.Worksheets.Item('10월')
  $v = $ws.Range('D7').Value2
  if ($v -ne $null) { "D7=" + $v + " (" + $v.GetType().Name + ")" } else { "D7=(비어 있음)" }
  "D12=" + $ws.Range('D12').Text + " / 값=" + $ws.Range('D12').Value2
  $wb.Close($false)
} finally { $xl.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl) }
```
통과: **D12 값이 1817000**이고 D7이 120000으로 읽히면(숫자 120000이든 글자 "120000"이든) 통과예요. (csv면 파일을 `Get-Content -Encoding UTF8`로 읽어 D7 자리가 `120000`인지 봐요.)
