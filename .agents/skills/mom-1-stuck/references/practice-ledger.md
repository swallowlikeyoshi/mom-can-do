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

**엑셀이 없거나 위 스크립트가 실패하면** 다시 실행하지 않고, 같은 내용을 `연습1_오류있는장부.csv`(UTF-8 BOM, `Out-File -Encoding UTF8`)로 만들어요. D7은 `="120,000원"`(엑셀이 숫자로 바꾸지 않게 글자 수식으로), D12는 `=D2+D3+...+D11` 문자열 그대로, E2는 `=#REF!`. 진도 맨 아래에 `화면 이름: 연습 파일 = csv`를 적어요.

## 확인 스크립트 (블록 2 확인 때, 한 번에 실행)

```powershell
$path = Join-Path (Join-Path ([Environment]::GetFolderPath('Desktop')) '엄마연습') '연습1_오류있는장부.xlsx'
$xl = New-Object -ComObject Excel.Application; $xl.Visible = $false; $xl.DisplayAlerts = $false
try {
  $wb = $xl.Workbooks.Open($path, 0, $true); $ws = $wb.Worksheets.Item('10월')
  "D7=" + $ws.Range('D7').Value2 + " (" + $ws.Range('D7').Value2.GetType().Name + ")"
  "D12=" + $ws.Range('D12').Text + " / 값=" + $ws.Range('D12').Value2
  $wb.Close($false)
} finally { $xl.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl) }
```
통과: D7이 `Double` 120000이고 D12 값이 1817000. (csv면 파일을 `Get-Content -Encoding UTF8`로 읽어 D7 자리가 `120000`인지 봐요.)
