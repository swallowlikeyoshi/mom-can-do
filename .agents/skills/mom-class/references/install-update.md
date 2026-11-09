# 업데이트 절차 ("엄마 강의 업데이트해줘")

저장소: `https://github.com/swallowlikeyoshi/mom-can-do`
설치 위치: `사용자폴더\.agents\skills\` (`Join-Path $HOME '.agents\skills'`)

## 원칙

- 바꾸는 건 설치 위치 안의 `mom-`으로 시작하는 폴더**만**이에요. 다른 스킬 폴더와 진도 파일(문서 폴더)은 건드리지 않아요.
- 내장 `skill-installer`는 업데이트에 쓰지 않아요. 다른 폴더에 설치해서 옛 강의와 새 강의가 둘 다 남을 수 있어요. 아래 스크립트만 써요.
- **아래 스크립트는 나누지 말고, PowerShell 한 번에 통째로 실행해요.** 명령마다 따로 실행하면 앞에서 만든 값이 사라져서 아무것도 복사되지 않아요.
- 스크립트는 git이 있으면 git으로, 없거나 실패하면 zip으로 한 번씩만 받아요. 다시 실행하지 않아요.
- 새 폴더를 `이름.new`로 먼저 복사한 다음에 옛 폴더와 바꿔요. 중간에 실패해도 옛 강의는 남아요.

## 스크립트

```powershell
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$repo = 'https://github.com/swallowlikeyoshi/mom-can-do'
$work = Join-Path $env:TEMP ('mom-can-do-' + (Get-Date -Format 'yyyyMMddHHmmss'))
New-Item -ItemType Directory -Force $work | Out-Null
$src = $null
$log = @()

if (Get-Command git -ErrorAction SilentlyContinue) {
  try {
    $gitDir = Join-Path $work 'git'
    & git clone --depth 1 -q $repo $gitDir 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { $src = Join-Path $gitDir '.agents\skills' } else { $log += "git 실패 (코드 $LASTEXITCODE)" }
  } catch { $log += "git 실패: $($_.Exception.Message)" }
} else { $log += 'git 없음' }

if (-not $src -or -not (Test-Path (Join-Path $src 'mom-class\SKILL.md'))) {
  try {
    $zip = Join-Path $work 'repo.zip'
    Invoke-WebRequest -UseBasicParsing -Uri "$repo/archive/refs/heads/main.zip" -OutFile $zip
    Expand-Archive $zip -DestinationPath (Join-Path $work 'zip')
    $src = Join-Path $work 'zip\mom-can-do-main\.agents\skills'
  } catch { $log += "zip 실패: $($_.Exception.Message)"; $src = $null }
}

if (-not $src -or -not (Test-Path (Join-Path $src 'mom-class\SKILL.md'))) {
  "실패: 강의 파일을 받지 못했어요"
  $log
  return
}

$dst = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Force $dst | Out-Null
$copied = @()
foreach ($d in Get-ChildItem $src -Directory -Filter 'mom-*') {
  $target = Join-Path $dst $d.Name
  $new = "$target.new"
  if (Test-Path $new) { Remove-Item $new -Recurse -Force }
  Copy-Item $d.FullName $new -Recurse
  if (Test-Path $target) { Remove-Item $target -Recurse -Force }
  Rename-Item $new $d.Name
  $copied += $d.Name
}
if ($copied.Count -eq 0) { "실패: 복사된 강의가 없어요"; return }
"성공: " + ($copied -join ', ')
$log
```

## 끝나면

- 출력이 **`성공:`으로 시작할 때만** 성공이에요. 복사된 이름 중 새로 생긴 강의를 쉬운 말로 알려드리고(예: "강의 1이 새로 생겼어요"), "ChatGPT 앱을 완전히 껐다가 다시 켜 주세요. 그다음 '엄마 강의'라고 하시면 돼요."
- 출력이 **`실패:`**면 다시 실행하지 않아요. "회사 인터넷에서 GitHub(강의 파일이 있는 곳)이 막혀 있는 것 같아요."라고 말하고 `mom-help`의 📨 요약을 만들자고 해요. 해본 것 칸에는 출력의 실패 줄(git, zip)을 한 줄씩 적어요.
