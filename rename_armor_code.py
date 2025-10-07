#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse
from pathlib import Path

def replace_names(root: Path, old_code: str, new_code: str):
    # 1) 파일명 먼저 변경
    file_count = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if old_code in fn:
                src = Path(dirpath) / fn
                dst = src.parent / fn.replace(old_code, new_code)
                if dst.exists():
                    # 동일 이름 이미 있으면 스킵
                    continue
                try:
                    src.rename(dst)
                    file_count += 1
                except Exception as e:
                    print(f"[WARN] 파일 이름 변경 실패: {src} -> {dst}: {e}", file=sys.stderr)

    # 2) 디렉토리명 변경 (깊은 경로부터)
    dir_count = 0
    all_dirs = [Path(p[0]) for p in os.walk(root)]
    for d in sorted(all_dirs, key=lambda x: len(str(x)), reverse=True):
        name = d.name
        if old_code in name:
            dst = d.parent / name.replace(old_code, new_code)
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

def parse_args():
    p = argparse.ArgumentParser(
        description="파일/디렉토리 이름에 포함된 코드를 일괄 치환합니다."
    )
    # 옵션 인자
    p.add_argument("--root", help="작업 루트 경로")
    p.add_argument("--old",  help="치환 전 코드 (예: 003)")
    p.add_argument("--new",  help="치환 후 코드 (예: 004)")
    # 위치 인자 (옵션 미사용 시 대체)
    p.add_argument("pos_root", nargs="?", help="작업 루트 경로(위치 인자)")
    p.add_argument("pos_old",  nargs="?", help="치환 전 코드(위치 인자)")
    p.add_argument("pos_new",  nargs="?", help="치환 후 코드(위치 인자)")
    a = p.parse_args()

    root = a.root or a.pos_root
    old_code = a.old or a.pos_old
    new_code = a.new or a.pos_new

    if not (root and old_code and new_code):
        p.error('인자 부족: --root/--old/--new 또는 위치 인자 <root> <old> <new> 형태로 입력하세요.')
    return Path(root), old_code, new_code

def main():
    root, old_code, new_code = parse_args()
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"경로가 존재하지 않거나 폴더가 아님: {root}")
        sys.exit(2)
    replace_names(root, old_code, new_code)

if __name__ == "__main__":
    main()
