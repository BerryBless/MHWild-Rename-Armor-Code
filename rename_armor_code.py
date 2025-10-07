#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from pathlib import Path

def replace_names(root: Path, old_code: str, new_code: str):
    # 파일명 먼저 변경
    file_count = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if old_code in fn:
                src = Path(dirpath) / fn
                dst = src.parent / fn.replace(old_code, new_code)
                if dst.exists():
                    continue
                try:
                    src.rename(dst)
                    file_count += 1
                except Exception as e:
                    print(f"[WARN] 파일 이름 변경 실패: {src} -> {dst}: {e}", file=sys.stderr)

    # 디렉토리명 변경 (하위부터)
    dir_count = 0
    all_dirs = [Path(p[0]) for p in os.walk(root)]
    for d in sorted(all_dirs, key=lambda x: len(str(x)), reverse=True):
        if old_code in d.name:
            dst = d.parent / d.name.replace(old_code, new_code)
            if dst.exists():
                continue
            try:
                d.rename(dst)
                dir_count += 1
            except Exception as e:
                print(f"[WARN] 디렉토리 이름 변경 실패: {d} -> {dst}: {e}", file=sys.stderr)

    print(f"파일 이름 변경: {file_count}개")
    print(f"디렉토리 이름 변경: {dir_count}개")
    print("모든 코드 치환 완료.")

def main():
    if len(sys.argv) < 4:
        print("사용법: python rename_armor_code.py <root_path> <old> <new>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    old_code = sys.argv[2]
    new_code = sys.argv[3]

    if not root.exists() or not root.is_dir():
        print(f"경로가 존재하지 않거나 폴더가 아님: {root}")
        sys.exit(2)

    replace_names(root, old_code, new_code)

if __name__ == "__main__":
    main()
