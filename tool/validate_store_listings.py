# -*- coding: utf-8 -*-
"""
Google Play Console Multi-language Store Listing Generator & Validator
Validates:
- App Name <= 30 chars
- Short Description <= 80 chars
- Full Description <= 4000 chars
"""

listings = {
    "ko-KR": {
        "lang_name": "한국어 (기본값)",
        "app_name": "물타기 계산기 - 주식 코인 평단가 계산기",
        "short_desc": "마이너스 계좌 탈출! 주식·코인 스마트 물타기 및 목표 평단가 역산 시뮬레이터",
        "full_desc": """📉 "물타기 잘못해서 마이너스 계좌가 더 깊어지셨나요?"
물타기는 감이나 운이 아닙니다. 철저한 수학적 데이터와 전략입니다!

'물타기 계산기'는 주식(국내/해외)과 가상자산(코인) 투자자를 위해 탄생한 차세대 스마트 DCA(Dollar-Cost Averaging) 평단가 관리 비서입니다.

지금 즉시 감으로 하는 매수를 멈추고, 완벽한 탈출 및 익절 시나리오를 설계해 보세요!

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 다운로드가 폭발하는 핵심 기능
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ 초정밀 물타기 시뮬레이터 (Smart DCA)
• 현재 보유 평단가와 수량, 추가 매수 가격만 입력하면 즉시 최종 평단가와 총 매수 금액 자동 계산.
• 실시간 인터랙티브 슬라이더로 매수 수량 조절에 따른 평단가 변화를 1초 만에 시각적으로 확인.
• 단계별 분할 매수 시나리오를 비교하여 나에게 가장 유리한 매수 플랜 수립.

2️⃣ 목표 평단가 역산 시뮬레이터 (Target Recovery Inversion)
• "내 평단가를 이 가격까지 낮추려면 대체 얼마를 더 사야 하지?"
• 원하는 목표 평단가(탈출 단가)를 입력하면 필요한 추가 매수 수량과 총알(예수금)을 1초 만에 역산!
• 무리한 물타기를 사전에 방지하고 계획적인 자금 배분을 실현합니다.

3️⃣ 0.2초 초고속 음성 입력 도크 (Voice Quick Dock)
• 키패드로 하나하나 입력하기 귀찮으셨나요?
• "삼성전자 5만 원에 100주"처럼 말 한마디로 즉시 계산 완료!
• 시장이 급변할 때 가장 빠르게 대응할 수 있는 혁신적인 음성 UX.

4️⃣ 100% 온디바이스 로컬 보안 (Zero Server Leak)
• 회원가입이나 로그인이 전혀 필요 없습니다.
• 여러분의 소중한 자산, 평단가, 보유 수량 데이터는 외부 서버로 1바이트도 전송되지 않습니다.
• 기기 내부 로컬 스토리지에만 100% 안전하게 암호화 보관됩니다.

5️⃣ 삼성 One UI 스타일의 프리미엄 금융 대시보드
• 눈이 편안한 다크모드 및 고대비 OLED 테마 기본 지원.
• 3D 반응형 차트와 카드 기반 인포그래픽으로 복잡한 금융 수치를 직관적으로 파악.
• 스마트폰은 물론 폴더블 폰, 7인치/10인치 태블릿 대화면까지 완벽 지원.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 이런 자산에 모두 사용 가능합니다!
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 국내 주식: 코스피(KOSPI), 코스닥(KOSDAQ) 전 종목
• 해외 주식: 미국 나스닥(NASDAQ), S&P 500, 뉴욕증시(NYSE)
• 가상자산 / 코인: 비트코인(BTC), 이더리움(ETH), 알트코인 전 종목
• ETF / 지수 펀드: 레버리지, 인버스, 배당주 ETF 등

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 이런 투자자분들께 강력 추천합니다!
━━━━━━━━━━━━━━━━━━━━━━━━━━
✔ 고점에 물려 본전 탈출(탈출가) 계산이 막막하신 분
✔ 분할 매수할 자금이 한정되어 최적의 매수량을 알고 싶으신 분
✔ 복잡한 엑셀(Excel)이나 일반 계산기 두드리다 지치신 분
✔ 내 계좌 정보가 유출될 걱정 없는 안전한 계산기를 원하시는 분

더 이상 손실에 불안해하지 마세요. 
지금 '물타기 계산기'를 다운로드하고, 가장 스마트한 성공 투자의 길을 시작하세요!

※ 본 애플리케이션은 투자 판단을 돕기 위한 보조 시뮬레이션 계산 도구이며, 원금 보장이나 투자 권유를 목적으로 하지 않습니다."""
    },
    "en-US": {
        "lang_name": "English (US)",
        "app_name": "DCA Calculator: Stock & Crypto",
        "short_desc": "Escape the red! Smart stock & crypto DCA calculator & target price simulator.",
        "full_desc": """📉 "Tired of averaging down blindly and watching losses grow?"
Smart investing isn't about guesswork—it's about math and disciplined strategy!

'DCA Calculator' is the ultimate smart Dollar-Cost Averaging assistant designed for stock and crypto investors worldwide. Plan your exit, lower your average entry price, and turn red days into profit!

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 KEY FEATURES BUILT TO WIN
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Precision Average Down Simulator (Smart DCA)
• Enter your current shares, average price, and new buy price to instantly calculate your updated breakeven point.
• Real-time interactive slider lets you visualize price changes dynamically.
• Compare multiple buyback scenarios to find the optimal cash allocation.

2️⃣ Target Price Inversion Engine
• "How much cash and how many shares do I need to drop my average to $X?"
• Simply input your desired target exit price, and our engine reverse-engineers the exact shares and capital required in seconds!
• Avoid over-investing and manage your risk with mathematical confidence.

3️⃣ 0.2s Voice Quick Dock
• Skip tedious keypad typing during fast-moving market dips.
• Speak your numbers naturally (e.g., "100 shares at 50 dollars") and let the voice dock calculate instantly.
• Fastest response time when every second counts.

4️⃣ 100% On-Device Privacy Guaranteed
• No sign-up, no login, and zero tracking.
• Your financial records, holdings, and portfolio numbers NEVER leave your phone.
• Stored securely only in your device's local memory.

5️⃣ Sleek Samsung One UI Inspired Dashboard
• Optimized Dark Mode and high-contrast OLED financial theme.
• Dynamic 3D interactive charts and intuitive card infographics.
• Flawlessly responsive across smartphones, foldables, and tablets.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUPPORTS ALL ASSETS WORLDWIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Global Stocks: NYSE, NASDAQ, S&P 500, ETFs
• Crypto: Bitcoin (BTC), Ethereum (ETH), and major altcoins
• Forex, Commodities & Index funds

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 WHO IS THIS APP FOR?
━━━━━━━━━━━━━━━━━━━━━━━━━━
✔ Bag holders looking for a calculated breakeven exit strategy
✔ Long-term DCA investors building wealth through market dips
✔ Traders tired of complicated spreadsheets and clumsy calculators
✔ Privacy-first investors who refuse to share portfolio data with servers

Take control of your portfolio today.
Download 'DCA Calculator' now and trade with mathematical precision!

*Disclaimer: This app is a financial simulation utility and does not constitute investment advice."""
    },
    "ja-JP": {
        "lang_name": "日本語 (ja-JP)",
        "app_name": "ナンピン計算機 - 株式 暗号資産 平均単価",
        "short_desc": "含み損からの脱出！株式・暗号資産のスマートなナンピン計算＆目標取得単価シミュレーター",
        "full_desc": """📉「ナンピン買いを焦って、さらに含み損を広げていませんか？」
ナンピン（難平）は勘や感情で行うものではありません。徹底した数学的計算と戦略が必要です！

『ナンピン計算機』は、日本株・米国株・暗号資産（仮想通貨）投資家のために開発された次世代スマートDCA計算アシスタントです。

曖昧な追加購入をやめて、確実な元本回収（脱出）および利益確定シナリオを設計しましょう！

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 ダウンロードを加速させる強力な機能
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ 高精度ナンピンシミュレーター（Smart DCA）
• 現在の保有株数・取得単価・追加買付価格を入力するだけで、新しい平均取得単価と必要資金を瞬時に自動計算。
• インタラクティブなスライダー操作で、買増し数量による平均単価の低下幅をリアルタイムに視覚化。
• 複数の分割買付シナリオを比較し、最もリスクの低い購入プランを導き出します。

2️⃣ 目標取得単価の逆算エンジン（脱出価格計算）
•「平均単価をこの価格まで下げるには、あと何株・いくら買えばいいの？」
• 希望する目標脱出単価を入力すれば、必要な追加株数と買付代金をわずか1秒で逆算！
• 資金ショートや無理な買い増しを防ぎ、計画的なトレードを実現します。

3️⃣ 0.2秒高速音声入力ドック
• 急変動する相場の中でテンキーをポチポチ打つ手間を解消！
•「トヨタ 100株 2000円」と話しかけるだけで、瞬時に数値を認識して自動計算。
• タイミングを逃さない最速の入力体験を提供します。

4️⃣ 100%端末内ローカル完結・安心のプライバシー
• 会員登録やログインは一切不要。
• お客様の資産情報や保有データは外部サーバーへ一切送信されません。
• 端末内のローカルストレージにのみ暗号化されて安全に保管されます。

5️⃣ One UIスタイルの洗練された金融ダッシュボード
• 目に優しいダークモードおよび高コントラストOLEDデザイン。
• 3Dグラフとカード型インフォグラフィックで計算結果を一目瞭然に表示。
• スマートフォンから折りたたみ端末、タブレットまで完全対応。

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 幅広い金融資産に対応
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 日本株（東証プライム・スタンダード・グロース）
• 米国株（NASDAQ、S&P 500、NYSE、ETF）
• 暗号資産・仮想通貨（ビットコイン、イーサリアム、アルトコイン全般）

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 こんな投資家におすすめ！
━━━━━━━━━━━━━━━━━━━━━━━━━━
✔ 塩漬け株の救出プラン・脱出計算を行いたい方
✔ 手元資金に合わせて最も効果的なナンピン数量を知りたい方
✔ エクセルや電卓での面倒な手計算から解放されたい方
✔ 資産データをサーバーに預けたくない安全重視の方

今すぐ『ナンピン計算機』をインストールして、勝率を高めるスマートな投資を始めましょう！

※ 本アプリは投資判断を支援するための計算シミュレーションツールであり、投資勧誘や元本保証を行うものではありません。"""
    },
    "zh-CN": {
        "lang_name": "中文（简体）(zh-CN)",
        "app_name": "补仓计算器 - 股票加密货币成本均价",
        "short_desc": "摆脱深套！股票与加密资产智能补仓成本测算，目标均价逆向推算解套神器。",
        "full_desc": """📉 “盲目补仓导致越补越套、越陷越深？”
聪明的投资从不凭直觉，而是依靠严谨的数学模型与资金策略！

《补仓计算器》是专为A股、美股、港股及加密货币投资者量身打造的智能DCA持仓成本管理神器。助你精准测算补仓成本，推导解套路线，将亏损逆转为盈利！

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 核心爆款功能
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ 精准补仓模拟器（Smart DCA）
• 输入当前持仓价格、持仓数量与计划补仓价，0.1秒自动算出补仓后的全新持仓均价与所需资金。
• 交互式动态滑动条，实时拖动直观查看补仓数量对持仓成本的拉低效果。
• 多重补仓方案横向对比，助你选出最优资金配比。

2️⃣ 目标均价逆向测算引擎（智能解套）
• “我想把持仓成本拉低到某个目标价，到底需要补多少手、多少钱？”
• 只要输入你的目标解套价，引擎立即逆向推算出所需的精确股数与资金！
• 告别盲目补仓，将宝贵资金用在刀刃上。

3️⃣ 0.2秒极速语音录入
• 行情波动分秒必争，无需繁琐按键。
• 对着手机说出价格和数量，系统智能识别并秒级呈现计算结果。

4️⃣ 100%本地端安全保障（绝对私密）
• 无需注册，无需登录，无任何追踪。
• 您的所有资产、持仓数量及交易数据均仅保存在手机本地，绝不上发任何云端服务器。

5️⃣ 媲美三星One UI的豪华金融视觉交互
• 专为专业交易者打造的深色暗夜模式与高对比度界面。
• 3D图表与直观卡片展示，复杂金融数据一目了然。
• 完美适配折叠屏与各尺寸平板设备。

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 全面支持全球多类资产
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 全球股市：A股、港股、美股（纳斯达克、标普500）、ETF
• 加密资产：比特币（BTC）、以太坊（ETH）及各类主流代币

告别被套焦虑，理性掌控每一笔资金。
立即下载《补仓计算器》，用数据开启你的解套致胜之路！

*免责声明：本应用为金融辅助计算工具，不构成任何投资建议。"""
    },
    "zh-TW": {
        "lang_name": "中文（繁體）(zh-TW)",
        "app_name": "補倉計算器 - 台股美股加密貨幣均價",
        "short_desc": "拒絕套牢！台股、美股與加密貨幣智慧攤平成本，目標均價逆向試算解套神器。",
        "full_desc": """📉 「盲目攤平成本，結果越攤越平、套得更深？」
成功的投資不靠憑感覺，而是依靠精準的數學模型與資金策略！

《補倉計算器》是專為台股、美股及加密貨幣投資人打造的智慧DCA持股成本管理工具。精確試算補倉均價，推導最佳解套路徑，助你化被動為主動！

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 核心特色亮點
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ 高精準攤平試算（Smart DCA）
• 輸入目前持有均價、股數與預計加碼價格，瞬間計算出最新的平均成本與總投入金額。
• 互動式滑動條設計，即時拉動即可視覺化看見均價變化。
• 多組加碼情境同時對比，制定最具防禦力的加碼策略。

2️⃣ 目標均價逆向試算（解套反推）
• 「如果我想把成本壓到特定價位，到底還要買幾張、準備多少資金？」
• 只要設定目標出場價格，系統一秒反推所需購買股數與預備金，精準掌握資金需求！

3️⃣ 0.2秒極速語音輸入
• 盤中價格瞬息萬變，省去繁瑣鍵盤輸入。
• 支援語音快速指令，說出價格與數量即可自動完成試算。

4️⃣ 100% 裝置本機隱私保護
• 免註冊、免登入、無任何遠端追蹤。
• 所有資產紀錄與持股資料僅儲存於您的手機內部，絕不上傳外部伺服器。

5️⃣ One UI 精品質感介面
• 支援質感深色模式與高對比金融主題。
• 3D 圖表化呈現，數據一目了然。
• 完美適配折疊手機與平板大螢幕。

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 支援各類投資商品
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 股票市場：台股（上市/上櫃）、美股（那斯達克、S&P 500）、各類ETF
• 加密資產：比特幣 (BTC)、以太幣 (ETH) 及各主流虛擬幣

揮別被套焦慮，理智規劃每次加碼。
立即下載《補倉計算器》，用數學掌握解套制勝契機！

*免責聲明：本工具僅供策略試算參考，不代表任何投資保證或邀約。"""
    },
    "es-ES": {
        "lang_name": "Español (es-ES / es-419)",
        "app_name": "Calculadora DCA - Bolsa Cripto",
        "short_desc": "¡Sal del rojo! Simulador DCA para promediar acciones y cripto en minutos.",
        "full_desc": """📉 "¿Cansado de promediar a la baja a ciegas y ver cómo aumentan tus pérdidas?"
¡La inversión inteligente no es cuestión de suerte, sino de matemática y estrategia disciplinada!

'Calculadora DCA' es el asistente definitivo de Dollar-Cost Averaging diseñado para inversores de acciones y criptomonedas. Reduce tu precio medio de compra, planifica tu salida del mercado y vuelve a estar en verde.

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 FUNCIONES CLAVE PARA GANAR
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Simulador Preciso de Promediado (Smart DCA)
• Introduce tus acciones actuales, precio medio y nuevo precio de compra para calcular al instante tu nuevo punto de equilibrio.
• Deslizador interactivo en tiempo real para visualizar cómo baja tu precio medio al instante.
• Compara múltiples escenarios de compra para optimizar tu capital disponible.

2️⃣ Motor de Inversión de Precio Objetivo
• "¿Cuánto dinero y cuántas acciones necesito para bajar mi precio medio a $X?"
• Solo ingresa tu precio objetivo de salida y el motor calculará con precisión matemática las acciones exactas y el dinero necesario.
• Evita compras excesivas y gestiona tu riesgo con total control.

3️⃣ Dock de Voz Ultrarrápido de 0.2s
• Olvídate de escribir números en momentos de alta volatilidad.
• Di tus cifras en voz alta y deja que el dock reconozca y calcule al instante.

4️⃣ 100% Privacidad Local en el Dispositivo
• Sin registros, sin inicios de sesión y sin rastreo en la nube.
• Tus números, carteras e información financiera NUNCA salen de tu teléfono móvil.

5️⃣ Interfaz Premium Estilo Samsung One UI
• Modo oscuro impecable con gráficos de alto contraste OLED.
• Gráficos 3D interactivos e infografías limpias.
• Totalmente adaptada a móviles, plegables y tabletas.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SOPORTA TODAS TUS INVERSIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Bolsas Mundiales: Wall Street, NASDAQ, S&P 500, IBEX, ETFs
• Criptomonedas: Bitcoin (BTC), Ethereum (ETH) y altcoins principales

¡Toma el control de tu cartera de inversión hoy mismo!
Descarga 'Calculadora DCA' y optimiza tu estrategia de compra con precisión.

*Aviso legal: Esta aplicación es una herramienta de simulación financiera y no constituye asesoramiento financiero."""
    },
    "vi-VN": {
        "lang_name": "Tiếng Việt (vi-VN)",
        "app_name": "Máy tính DCA Cổ phiếu & Crypto",
        "short_desc": "Thoát lỗ nhanh chóng! Máy tính trung bình giá DCA cổ phiếu & crypto thông minh.",
        "full_desc": """📉 "Bạn mệt mỏi vì bắt đáy, trung bình giá sai khiến tài khoản ngày càng âm nặng?"
Đầu tư thành công không dựa vào cảm tính mà dựa trên số liệu toán học và kế hoạch dòng tiền!

'Máy tính DCA' là trợ lý quản lý giá vốn và trung bình giá (Dollar-Cost Averaging) thông minh hàng đầu dành cho nhà đầu tư chứng khoán và tiền điện tử (crypto). Giúp bạn tính toán kế hoạch về bờ nhanh nhất!

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 TÍNH NĂNG NỔI BẬT BỨT PHÁ
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Mô phỏng Trung Bình Giá Chuẩn Xác (Smart DCA)
• Nhập số lượng hiện tại, giá vốn và giá mua thêm để tính ngay giá vốn bình quân mới và tổng số tiền cần nạp.
• Thanh trượt tương tác trực quan giúp bạn thấy rõ sự thay đổi của giá vốn theo từng lượng mua thêm.
• So sánh nhiều kịch bản mua để chọn ra phương án tối ưu nhất.

2️⃣ Tính Ngược Giá Mục Tiêu (Chiến Lược Về Bờ)
• "Cần thêm bao nhiêu tiền và bao nhiêu cổ phiếu để hạ giá vốn về mức mình mong muốn?"
• Chỉ cần nhập mức giá mục tiêu, ứng dụng sẽ tự động tính ngược chính xác khối lượng và số vốn cần chuẩn bị trong 1 giây!
• Giúp bạn không bị cạn vốn và chủ động trước mọi nhịp giảm của thị trường.

3️⃣ Nhập Liệu Bằng Giọng Nói 0.2s Siêu Tốc
• Không cần bấm phím số phức tạp khi thị trường biến động nhanh.
• Chỉ cần nói giá và khối lượng, hệ thống sẽ tự động nhận diện và tính toán tức thì.

4️⃣ Bảo Mật 100% Trên Thiết Bị (Không Lưu Server)
• Không cần đăng ký, không cần đăng nhập.
• Dữ liệu tài sản và danh mục của bạn hoàn toàn lưu trữ cục bộ trên máy, tuyệt đối không gửi lên máy chủ bên ngoài.

5️⃣ Giao Diện One UI Đẳng Cấp & Trực Quan
• Chế độ Dark Mode hiện đại, đồ họa 3D trực quan, tối ưu cho mắt khi theo dõi bảng điện tử.
• Tương thích mượt mà trên điện thoại, màn hình gập và máy tính bảng.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 HỖ TRỢ ĐA DẠNG DANH MỤC
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Chứng khoán: VN-Index (Việt Nam), Chứng khoán Mỹ (NASDAQ, S&P 500), Chứng chỉ quỹ ETF
• Tiền mã hóa / Crypto: Bitcoin (BTC), Ethereum (ETH) và các Altcoin

Chấm dứt nỗi lo kẹp hàng!
Tải ngay 'Máy tính DCA' để làm chủ chiến lược bắt đáy và về bờ an toàn!

*Tuyên bố miễn trừ trách nhiệm: Ứng dụng là công cụ tính toán hỗ trợ mô phỏng, không cấu thành lời khuyên đầu tư tài chính."""
    },
    "id-ID": {
        "lang_name": "Bahasa Indonesia (id-ID)",
        "app_name": "Kalkulator DCA Saham & Kripto",
        "short_desc": "Atasi kerugian! Kalkulator DCA saham & kripto pintar serta simulasi target cuan.",
        "full_desc": """📉 "Sering average down sembarangan hingga modal habis dan portofolio makin merah?"
Investasi cerdas tidak mengandalkan tebakan, melainkan perhitungan matematis yang matang!

'Kalkulator DCA' adalah asisten pintar Dollar-Cost Averaging (DCA) yang dirancang khusus untuk investor saham (IHSG, AS) dan aset kripto. Rencanakan strategi keluar dan turunkan harga rata-rata portofolio Anda dengan tepat!

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 FITUR UNGGULAN UNTUK MAKSIMALKAN CUAN
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Simulator Average Down Akurat (Smart DCA)
• Masukkan jumlah lot/koin, harga beli lama, dan harga beli baru untuk menghitung harga rata-rata (breakeven) seketika.
• Slider interaktif memungkinkan Anda melihat perubahan harga rata-rata secara dinamis dan visual.
• Bandingkan berbagai skenario pembelian agar alokasi modal Anda lebih terukur.

2️⃣ Mesin Hitung Balik Target Harga (Strategi Balik Modal)
• "Berapa banyak uang dan lot yang dibutuhkan untuk menurunkan harga rata-rata ke angka target?"
• Cukup masukkan target harga yang diinginkan, dan kalkulator akan menghitung balik jumlah lot serta dana yang harus disiapkan dalam 1 detik!
• Hindari kehabisan amunisi di tengah jalan dengan perencanaan yang pasti.

3️⃣ Input Suara Cepat 0.2 Detik
• Tak perlu repot mengetik saat pergerakan harga pasar sedang cepat.
• Sebutkan jumlah dan harga secara alami, aplikasi akan otomatis memproses perhitungannya.

4️⃣ 100% Privasi di Perangkat Anda (Tanpa Server)
• Tanpa daftar akun, tanpa login, dan bebas pelacakan.
• Seluruh catatan aset dan investasi Anda tersimpan aman hanya di memori HP Anda sendiri.

5️⃣ Tampilan Premium Bergaya Samsung One UI
• Dilengkapi Dark Mode hemat baterai dan grafis 3D modern.
• Tampilan infografis kartu yang sangat mudah dipahami.
• Responsif untuk smartphone, ponsel lipat, hingga tablet.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 DUKUNGAN SEMUA ASET INVESTASI
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pasar Saham: Saham Indonesia (IHSG/IDX), Pasar Saham Global (NASDAQ, NYSE), Reksa Dana & ETF
• Kripto: Bitcoin (BTC), Ethereum (ETH), dan berbagai Altcoin populer

Jangan biarkan portofolio merah berlarut-larut.
Download 'Kalkulator DCA' sekarang dan kelola strategi average down Anda secara profesional!

*Pernyataan Penolakan: Aplikasi ini adalah alat bantu simulasi finansial dan bukan merupakan nasihat investasi keuangan."""
    }
}

# Validation & File Output
with open("store/store_listing_multilingual.txt", "w", encoding="utf-8") as f_multi, \
     open("store/store_listing.txt", "w", encoding="utf-8") as f_default:
    
    f_multi.write("====================================================\n")
    f_multi.write(" Google Play Console Multi-language Store Listings  \n")
    f_multi.write(" ASO Optimization (High-Conversion / Viral Downloads)\n")
    f_multi.write("====================================================\n\n")

    for code, data in listings.items():
        name_len = len(data["app_name"])
        short_len = len(data["short_desc"])
        full_len = len(data["full_desc"])
        
        name_ok = name_len <= 30
        short_ok = short_len <= 80
        full_ok = full_len <= 4000
        
        status = "OK" if (name_ok and short_ok and full_ok) else "FAILED"
        print(f"[{code}] Length check: Name={name_len}/30, Short={short_len}/80, Full={full_len}/4000 -> {status}")
        
        # Write to multi file
        f_multi.write(f"####################################################\n")
        f_multi.write(f"### [{code}] {data['lang_name']}\n")
        f_multi.write(f"####################################################\n\n")
        f_multi.write(f"[1. 앱 이름 (App Name) - {name_len}/30자]\n")
        f_multi.write(f"{data['app_name']}\n\n")
        f_multi.write(f"[2. 간단한 설명 (Short Description) - {short_len}/80자]\n")
        f_multi.write(f"{data['short_desc']}\n\n")
        f_multi.write(f"[3. 자세한 설명 (Full Description) - {full_len}/4000자]\n")
        f_multi.write(f"{data['full_desc']}\n\n\n")

        # Write default ko-KR to store_listing.txt
        if code == "ko-KR":
            f_default.write(f"[구글 플레이 스토어 기본 등록정보 (ko-KR)]\n\n")
            f_default.write(f"■ 앱 이름 ({name_len}/30자)\n")
            f_default.write(f"{data['app_name']}\n\n")
            f_default.write(f"■ 간단한 설명 ({short_len}/80자)\n")
            f_default.write(f"{data['short_desc']}\n\n")
            f_default.write(f"■ 자세한 설명 ({full_len}/4000자)\n")
            f_default.write(f"{data['full_desc']}\n")

print("\nStore listings successfully exported to store/store_listing_multilingual.txt and store/store_listing.txt!")

