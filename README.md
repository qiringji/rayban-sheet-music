# rayban-sheet-music

Meta Ray-Ban スマートグラスのディスプレイに楽譜を表示するアプリケーションです。

## 概要

このプロジェクトは、Meta Ray-Ban Display API を利用して、MusicXML / MusicJSON 形式の楽譜データをメガネのディスプレイにリアルタイムで表示します。演奏中に手を使わずに次の小節を確認できます。

参考プロジェクト: [claude-glasses](https://github.com/qiringji/claude-glasses) — Claude / Whisper / TTS を活用した iOS 音声アシスタント

## 特徴

- Meta Ray-Ban Display API 経由で楽譜を HUD 表示
- - MusicXML / ABC Notation をサポート
  - - 小節単位でのページ送り（ハンズフリー）
    - - BLE 接続によるスマートフォンとの連携
      - - Python バックエンド + iOS コンパニオンアプリ
       
        - ## アーキテクチャ
       
        - ```
          ┌─────────────────────┐        BLE / Wi-Fi        ┌──────────────────────┐
          │   iOS Companion App │ ◀────────────────────────▶ │  Meta Ray-Ban Glasses │
          │  (SwiftUI / Tuist)  │                            │  (Display API)        │
          └─────────┬───────────┘                            └──────────────────────┘
                    │ REST / WebSocket
                    ▼
          ┌─────────────────────┐
          │   Python Backend    │
          │  - Score Parser     │
          │  - Renderer         │
          │  - Playback Sync    │
          └─────────────────────┘
          ```

          ## ディレクトリ構成

          ```
          rayban-sheet-music/
          ├── backend/               # Python バックエンドサーバー
          │   ├── main.py            # FastAPI エントリーポイント
          │   ├── parser/            # MusicXML / ABC 楽譜パーサー
          │   │   ├── musicxml.py
          │   │   └── abc_notation.py
          │   ├── renderer/          # 楽譜レンダリングエンジン
          │   │   └── score_renderer.py
          │   └── display/           # Meta Ray-Ban Display API クライアント
          │       └── rayban_client.py
          ├── ios/                   # iOS コンパニオンアプリ (SwiftUI + Tuist)
          │   ├── Project.swift
          │   ├── Tuist/
          │   │   └── Package.swift
          │   └── Sources/
          │       ├── App/
          │       ├── Views/
          │       └── Clients/
          │           ├── DisplayClient.swift
          │           └── BluetoothClient.swift
          ├── scores/                # サンプル楽譜データ
          │   └── sample.musicxml
          ├── docs/                  # 設計ドキュメント
          │   ├── architecture.md
          │   └── display-api.md
          ├── AGENTS.md              # AI エージェント向け指示
          └── README.md
          ```

          ## セットアップ

          ### 必要環境

          - Python 3.11+
          - - Xcode 15+
            - - Tuist 4+
              - - Meta Ray-Ban グラス（Display API 対応モデル）
               
                - ### バックエンドのセットアップ
               
                - ```bash
                  git clone https://github.com/qiringji/rayban-sheet-music.git
                  cd rayban-sheet-music/backend
                  pip install -r requirements.txt
                  cp .env.template .env
                  # .env に Meta Display API キーを設定
                  uvicorn main:app --reload
                  ```

                  ### iOS アプリのセットアップ

                  ```bash
                  cd ios
                  tuist install
                  tuist generate
                  open RayBanSheetMusic.xcworkspace
                  ```

                  ## 使い方

                  1. バックエンドサーバーを起動する
                  2. 2. iOS アプリを起動し、BLE で Ray-Ban グラスとペアリングする
                     3. 3. 楽譜ファイル（MusicXML）をアップロードする
                        4. 4. 再生・ページ送りの操作をする
                          
                           5. ## 技術スタック
                          
                           6. | レイヤー | 技術 |
                           7. |---|---|
                           8. | バックエンド | Python, FastAPI, music21 |
                           9. | 楽譜パース | music21, abcjs |
                           10. | iOS アプリ | SwiftUI, Tuist, Combine |
                           11. | グラス表示 | Meta Ray-Ban Display API |
                           12. | 通信 | BLE, WebSocket |
                          
                           13. ## ライセンス
                          
                           14. MIT License — 詳細は [LICENSE](LICENSE) を参照してください。
