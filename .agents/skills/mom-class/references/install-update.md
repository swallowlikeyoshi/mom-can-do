# 업데이트 절차 ("엄마 강의 업데이트해줘")

저장소: `https://github.com/swallowlikeyoshi/mom-can-do`
설치 위치: `사용자폴더\.agents\skills\` (`Join-Path $HOME '.agents\skills'`)

## 원칙

- 바꾸는 건 설치 위치 안의 `mom-`으로 시작하는 폴더**만**이에요. 다른 스킬 폴더와 진도 파일(문서 폴더)은 건드리지 않아요.
- 새 파일을 다 받은 **다음에** 옛 `mom-*` 폴더를 지우고 새 것으로 바꿔요. 받다가 실패하면 옛 것은 그대로 둬요.
- 아래 세 방법을 순서대로 **한 번씩만** 시도해요. 같은 방법을 다시 하지 않아요.

## 방법

1. **skill-installer**: 내장 `skill-installer`로 위 저장소의 `.agents/skills/` 아래 `mom-*` 스킬을 설치(덮어쓰기)해요.
2. **git**: `git --version`이 되면
   ```powershell
   $tmp = Join-Path $env:TEMP 'mom-can-do'
   if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
   git clone --depth 1 https://github.com/swallowlikeyoshi/mom-can-do $tmp
   $src = Join-Path $tmp '.agents\skills'
   ```
3. **zip 내려받기**:
   ```powershell
   $zip = Join-Path $env:TEMP 'mom-can-do.zip'
   $out = Join-Path $env:TEMP 'mom-can-do-zip'
   Invoke-WebRequest -Uri https://github.com/swallowlikeyoshi/mom-can-do/archive/refs/heads/main.zip -OutFile $zip
   if (Test-Path $out) { Remove-Item $out -Recurse -Force }
   Expand-Archive $zip -DestinationPath $out
   $src = Join-Path $out 'mom-can-do-main\.agents\skills'
   ```

2나 3으로 `$src`를 얻었으면:
```powershell
$dst = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Force $dst | Out-Null
Get-ChildItem $src -Directory -Filter 'mom-*' | ForEach-Object {
  $target = Join-Path $dst $_.Name
  if (Test-Path $target) { Remove-Item $target -Recurse -Force }
  Copy-Item $_.FullName $target -Recurse
}
```

## 끝나면

- 성공: 바뀐 스킬 이름을 쉬운 말로 알려드리고(예: "강의 1이 새로 생겼어요"), "ChatGPT 앱을 완전히 껐다가 다시 켜 주세요. 그다음 '엄마 강의'라고 하시면 돼요."
- 셋 다 실패: "회사 인터넷에서 GitHub(강의 파일이 있는 곳)이 막혀 있는 것 같아요." 그리고 `mom-help`의 📨 요약을 만들자고 해요. 해본 것 칸에 세 방법과 각각의 오류를 한 줄씩 적어요.
