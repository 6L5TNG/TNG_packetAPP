import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class PatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TNG Auto Patcher v3.0 (Single Backup)")
        self.root.geometry("700x600")
        
        # 현재 프로젝트 경로 (TNG_packetAPP_Dev)
        self.current_dir = Path(os.getcwd())
        # 상위 폴더 (TNG_packetAPP)
        self.parent_dir = self.current_dir.parent
        
        # 백업 저장소 설정 (항상 같은 이름 'Latest_Backup' 사용)
        # 위치: ../Backup/Latest_Backup
        self.backup_root = self.parent_dir / "Backup"
        self.latest_backup_dir = self.backup_root / "Latest_Backup"

        # --- UI 구성 ---
        tk.Label(root, text="Copilot 패치 코드를 붙여넣으세요.", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        
        # 안내 문구
        info_text = (f"※ 패치 전, 이전 백업을 삭제하고 현재 상태를 덮어씁니다.\n"
                     f"※ 백업 위치: {self.latest_backup_dir}\n"
                     f"※ 백업 파일은 GitHub에 절대 올라가지 않습니다.")
        tk.Label(root, text=info_text, fg="blue", justify="center", font=("Arial", 9)).pack(pady=(0, 10))
        
        self.text_area = scrolledtext.ScrolledText(root, height=15, width=80)
        self.text_area.pack(padx=10, pady=5)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)
        
        # 버튼들
        self.btn_apply = tk.Button(btn_frame, text="💾 백업(덮어쓰기) 후 패치", command=self.run_patch_process, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=25, height=2)
        self.btn_apply.pack(side=tk.LEFT, padx=10)

        self.btn_upload = tk.Button(btn_frame, text="☁️ GitHub 업로드", command=self.upload_to_github, bg="#2196F3", fg="white", font=("Arial", 11, "bold"), width=25, height=2)
        self.btn_upload.pack(side=tk.LEFT, padx=10)
        
        tk.Label(root, text="작업 로그:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(root, height=8, width=90, state='disabled', bg="#f0f0f0")
        self.log_area.pack(padx=10, pady=(0, 10))

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def run_patch_process(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("경고", "패치할 코드가 없습니다.")
            return

        # 데이터 파싱
        try:
            try:
                patch_data = json.loads(content)
            except:
                patch_data = eval(content)
            
            if not isinstance(patch_data, dict):
                raise ValueError("데이터 형식이 딕셔너리가 아닙니다.")
        except Exception as e:
            messagebox.showerror("에러", f"코드 형식이 올바르지 않습니다.\n{e}")
            return

        # --- 1. 백업 수행 (덮어쓰기) ---
        try:
            self.log("백업 시작...")
            
            # 백업 루트 폴더가 없으면 생성
            if not self.backup_root.exists():
                self.backup_root.mkdir()
            
            # 기존 백업이 있으면 '삭제' (이게 덮어쓰기의 핵심)
            if self.latest_backup_dir.exists():
                self.log("이전 백업 삭제 중...")
                shutil.rmtree(self.latest_backup_dir)
            
            # 현재 상태 복사
            shutil.copytree(self.current_dir, self.latest_backup_dir, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
            self.log(f"✅ 새 백업 완료: Latest_Backup")
            
        except Exception as e:
            messagebox.showerror("백업 실패", f"백업 중 오류가 발생했습니다.\n{e}")
            self.log(f"❌ 백업 실패: {e}")
            return

        # --- 2. 패치 적용 ---
        try:
            self.log("패치 적용 시작...")
            count = 0
            for filename, file_content in patch_data.items():
                path = self.current_dir / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(file_content.strip() + "\n")
                self.log(f" - 수정됨: {filename}")
                count += 1
            
            self.log(f"✅ 패치 완료! ({count}개 파일)")
            messagebox.showinfo("성공", f"백업(덮어쓰기) 및 패치가 완료되었습니다!")
            
        except Exception as e:
            messagebox.showerror("패치 에러", f"파일 쓰기 중 오류 발생:\n{e}")
            self.log(f"❌ 패치 에러: {e}")

    def upload_to_github(self):
        try:
            self.log("GitHub 업로드 시작...")
            
            # .gitignore 파일 확인 (혹시 모를 사고 방지용)
            gitignore_path = self.current_dir / ".gitignore"
            if not gitignore_path.exists():
                with open(gitignore_path, "w") as f:
                    f.write("__pycache__/\n*.pyc\n")
            
            subprocess.run(["git", "add", "."], check=True, cwd=self.current_dir)
            
            msg = f"Update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", msg], check=True, cwd=self.current_dir)
            
            self.log("서버로 전송 중 (Push)...")
            subprocess.run(["git", "push", "origin", "main"], check=True, cwd=self.current_dir)
            
            self.log("✅ GitHub 업로드 성공!")
            messagebox.showinfo("GitHub", "성공적으로 업로드되었습니다!")
            
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Git 명령 오류: {e}")
            messagebox.showerror("Git 에러", "변경사항이 없거나 오류가 발생했습니다.\n(로그 확인)")
        except Exception as e:
            self.log(f"❌ 시스템 오류: {e}")
            messagebox.showerror("에러", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PatcherApp(root)
    root.mainloop()