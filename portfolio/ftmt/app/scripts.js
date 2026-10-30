// Tarot Card Data
const tarotCards = [
  {
    title: "XVII. THE STAR (별)",
    img: "assets/images/tarot_star.jpg",
    desc: "어둠을 뚫고 쏟아지는 치유와 희망의 영감입니다. 당신의 직관과 내면의 목소리를 신뢰하세요. 오랫동안 풀리지 않던 금전 및 진로의 고민에 명쾌한 돌파구가 열립니다."
  },
  {
    title: "XIX. THE SUN (태양)",
    img: "assets/images/tarot_sun.jpg",
    desc: "찬란한 에너지와 확실한 성공, 도파민 넘치는 승리의 기운입니다. 오늘 시도하는 새로운 도전과 인연은 매우 긍정적인 결과와 따뜻한 결실을 맺을 것입니다."
  },
  {
    title: "X. WHEEL OF FORTUNE (운명의 수레바퀴)",
    img: "assets/images/tarot_wheel.jpg",
    desc: "우주적 전환점과 대운(大運)의 주기적 흐름입니다. 예상치 못한 귀인의 도움이나 인연의 극적인 발전이 찾아오니 기회를 주저하지 말고 쟁취하세요."
  }
];

let currentCardIdx = 0;
let isFlipped = false;
let hearts = 7;

// Switch Main Views (Landing vs Web App)
function switchView(viewName) {
  const landing = document.getElementById('landingView');
  const webapp = document.getElementById('webAppView');
  const tabLanding = document.getElementById('tabLanding');
  const tabWebApp = document.getElementById('tabWebApp');

  if (viewName === 'webapp') {
    landing.classList.remove('active');
    webapp.classList.add('active');
    tabLanding.classList.remove('active');
    tabWebApp.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    webapp.classList.remove('active');
    landing.classList.add('active');
    tabWebApp.classList.remove('active');
    tabLanding.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Carousel Mockup Switcher
function setMockup(src, btn) {
  const img = document.getElementById('mockupImage');
  img.style.opacity = '0.3';
  setTimeout(() => {
    img.src = src;
    img.style.opacity = '1';
  }, 150);

  document.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// Switch App Features inside Web App
function switchAppTab(tabName, btn) {
  document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
  document.querySelectorAll('.app-tab').forEach(tb => tb.classList.remove('active'));

  if (tabName === 'tarot') {
    document.getElementById('tabTarot').classList.add('active');
  } else if (tabName === 'dopamine') {
    document.getElementById('tabDopamine').classList.add('active');
  } else if (tabName === 'match') {
    document.getElementById('tabMatch').classList.add('active');
  }
  btn.classList.add('active');
}

// Tarot Actions
function flipTarot() {
  const card = document.getElementById('tarotCard');
  isFlipped = !isFlipped;
  if (isFlipped) {
    card.classList.add('flipped');
  } else {
    card.classList.remove('flipped');
  }
}

function pickCard(idx, btn) {
  currentCardIdx = idx;
  const cardData = tarotCards[idx];
  const card = document.getElementById('tarotCard');
  const cardImg = document.getElementById('tarotCardImg');
  const cardTitle = document.getElementById('cardTitle');
  const cardDesc = document.getElementById('cardDesc');

  if (btn) {
    document.querySelectorAll('.btn-pick').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }

  card.classList.remove('flipped');
  isFlipped = false;

  setTimeout(() => {
    cardImg.src = cardData.img;
    cardTitle.textContent = cardData.title;
    cardDesc.textContent = cardData.desc;
    card.classList.add('flipped');
    isFlipped = true;
  }, 350);
}

// Update Phone Status Bar Clock
function updateMockupTime() {
  const timeEl = document.getElementById('mockupTime');
  if (!timeEl) return;
  const now = new Date();
  const hrs = String(now.getHours()).padStart(2, '0');
  const mins = String(now.getMinutes()).padStart(2, '0');
  timeEl.textContent = `${hrs}:${mins}`;
}
setInterval(updateMockupTime, 1000);
updateMockupTime();

// Dopamine Daily Secret Engine (Changes Daily & Synchronized with Planetary Hours)
const dailyDopaminePool = [
  {
    time: "14:30 ~ 16:00",
    action: "중요한 계약 체결, 복권 구매, 또는 새로운 사업 프로젝트 제안에 최적의 금전운입니다.",
    caution: "감정적 기복이 심하거나 날카로운 말을 쏟아내는 화(火) 기운의 인물을 피하세요."
  },
  {
    time: "09:20 ~ 11:00",
    action: "문서 서명, 자산 재배치, 귀인과의 첫 미팅에서 놀라운 호감을 얻는 황금 시간대입니다.",
    caution: "과도한 욕심으로 즉흥적인 투자나 무리한 지출을 권유하는 상성을 경계하세요."
  },
  {
    time: "11:40 ~ 13:15",
    action: "자신의 재능과 아이디어를 대중이나 상사에게 어필할 때 도파민과 주목도가 폭발합니다.",
    caution: "말실수가 생기기 쉬우니 타인의 험담에 동조하지 말고 중립을 유지하세요."
  },
  {
    time: "16:40 ~ 18:20",
    action: "지연되던 협상이나 밀린 정산이 속 시원하게 해결되는 우주적 회수 주기입니다.",
    caution: "피로가 누적되어 판단력이 흐려질 수 있으니 음주 가무나 충동구매를 멀리하세요."
  },
  {
    time: "19:30 ~ 21:00",
    action: "소중한 인연과의 깊은 대화, 애정 고백, 진솔한 유대감을 형성하기에 가장 길합니다.",
    caution: "과거의 서운했던 기억이나 사소한 집착을 상대에게 강요하지 않도록 주의하세요."
  },
  {
    time: "07:30 ~ 09:00",
    action: "하루의 첫 승기를 잡는 시간. 아침 산책, 명상, 오늘의 핵심 1순위 업무에 집중하세요.",
    caution: "조급한 마음에 서두르면 소지품 분실이나 이동 중 작은 실수가 생길 수 있습니다."
  },
  {
    time: "21:30 ~ 23:00",
    action: "영적 통찰과 창의적 직관이 최고조에 달합니다. 아이디어 기록이나 타로 리딩에 최적입니다.",
    caution: "스마트폰을 너무 오래 보며 늦은 수면을 취하면 내일의 기운이 분산됩니다."
  }
];

let todayDopamineData = null;

// Initialize Daily Dopamine Secret based on Current Date
function updateDailyDopamine(seedOffset = 0) {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const day = now.getDate();

  // Create date seed so it changes automatically each midnight
  const dayIndex = (year * 365 + month * 31 + day + seedOffset) % dailyDopaminePool.length;
  todayDopamineData = dailyDopaminePool[Math.abs(dayIndex)];

  const monthNames = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];
  const dayOfWeekNames = ["일", "월", "화", "수", "목", "금", "토"];
  const dateStr = `${monthNames[month]} ${day}일 (${dayOfWeekNames[now.getDay()]})`;

  const dateBadge = document.getElementById('dopamineDateBadge');
  if (dateBadge) {
    dateBadge.textContent = `${dateStr} 오늘`;
  }

  const timeDisplay = document.getElementById('goldenTimeDisplay');
  if (timeDisplay) {
    timeDisplay.textContent = todayDopamineData.time;
  }

  const actionGuide = document.getElementById('dopamineActionGuide');
  if (actionGuide) {
    actionGuide.innerHTML = `<strong>✦ 오늘의 행운 행동:</strong> ${todayDopamineData.action}`;
  }

  const cautionGuide = document.getElementById('dopamineCautionGuide');
  if (cautionGuide) {
    cautionGuide.innerHTML = `<strong>⚠ 오늘의 주의 상성:</strong> ${todayDopamineData.caution}`;
  }
}

// Dopamine Hour Boost
function boostFortune() {
  if (!todayDopamineData) updateDailyDopamine();
  if (hearts > 0) {
    hearts--;
    document.getElementById('walletHearts').textContent = hearts;
    alert(`✨ 복채 하트 1개가 공양되었습니다!\n\n[우주 주파수 증폭 완료]\n오늘 ${todayDopamineData.time} 사이의 직관력과 금전운 에너지가 2.4배 증폭됩니다.`);
  } else {
    alert('보유 복채 하트가 부족합니다. 매일 자정에 무료 충전됩니다.');
  }
}

// Zodiac Calculator
function calculateMySign() {
  const input = document.getElementById('birthInput').value;
  if (!input) return;

  const date = new Date(input);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();

  const stems = ['갑(甲)', '을(乙)', '병(丙)', '정(丁)', '무(戊)', '기(己)', '경(庚)', '신(辛)', '임(壬)', '계(癸)'];
  const branches = ['자(子)', '축(丑)', '인(寅)', '묘(卯)', '진(辰)', '사(巳)', '오(午)', '미(未)', '신(申)', '유(酉)', '술(戌)', '해(亥)'];
  const animals = ['쥐띠', '소띠', '호랑이띠', '토끼띠', '용띠', '뱀띠', '말띠', '양띠', '원숭이띠', '닭띠', '개띠', '돼지띠'];

  const stemIdx = (year - 4) % 10;
  const branchIdx = (year - 4) % 12;

  let zodiac = '사자자리';
  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) zodiac = '물병자리';
  else if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) zodiac = '물고기자리';
  else if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) zodiac = '양자리';
  else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) zodiac = '황소자리';
  else if ((month === 5 && day >= 21) || (month === 6 && day <= 21)) zodiac = '쌍둥이자리';
  else if ((month === 6 && day >= 22) || (month === 7 && day <= 22)) zodiac = '게자리';
  else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) zodiac = '사자자리';
  else if ((month === 8 && day >= 23) || (month === 9 && day <= 23)) zodiac = '처녀자리';
  else if ((month === 9 && day >= 24) || (month === 10 && day <= 22)) zodiac = '천칭자리';
  else if ((month === 10 && day >= 23) || (month === 11 && day <= 22)) zodiac = '전갈자리';
  else if ((month === 11 && day >= 23) || (month === 12 && day <= 24)) zodiac = '사수자리';
  else zodiac = '염소자리';

  const resText = `${stems[Math.abs(stemIdx)]}${branches[Math.abs(branchIdx)]} · ${animals[Math.abs(branchIdx)]} · ${zodiac}`;
  document.getElementById('userCoordLabel').textContent = resText;
  document.getElementById('myMatchLabel').textContent = `${stems[Math.abs(stemIdx)]}${branches[Math.abs(branchIdx)]}`;

  // Recalculate daily dopamine hours customized to this user's birth sign
  updateDailyDopamine(day);
  updateMatchScore();

  alert(`우주 좌표가 갱신되었습니다:\n${resText}\n\n오늘 당신의 고유 도파민 골든 아워가 맞춤 갱신되었습니다.`);
}

// Match Score & Synergy Matrix
function updateMatchScore() {
  const select = document.getElementById('targetSelect');
  const val = select.value;
  const targetLabel = document.getElementById('targetMatchLabel');
  const targetElementTag = document.getElementById('targetElementTag');
  const scoreVal = document.getElementById('matchScoreVal');
  const scoreMeterFill = document.getElementById('scoreMeterFill');
  const scoreDesc = document.getElementById('matchScoreDesc');
  const harmonyVal = document.getElementById('harmonyVal');
  const energyVal = document.getElementById('energyVal');
  const frequencyVal = document.getElementById('frequencyVal');
  const tipText = document.getElementById('matchTipText');

  if (val === '계해') {
    targetLabel.textContent = '계해(癸亥)';
    if (targetElementTag) targetElementTag.textContent = '음수(陰水)';
    scoreVal.textContent = '96점';
    if (scoreMeterFill) scoreMeterFill.style.width = '96%';
    scoreDesc.textContent = '천생연분 우주 좌표의 만남';
    if (harmonyVal) harmonyVal.textContent = '무계합화(戊癸合火)';
    if (energyVal) energyVal.textContent = '상생 촉진 (大吉)';
    if (frequencyVal) frequencyVal.textContent = '99.2 MHz';
    tipText.textContent = '무토(戊土)와 계수(癸水)가 만나 무계합화(戊癸合火)를 이루는 최상의 연분입니다. 서로의 부족한 기운을 자연스럽게 채워주는 평생의 파트너입니다.';
  } else if (val === '갑자') {
    targetLabel.textContent = '갑자(甲子)';
    if (targetElementTag) targetElementTag.textContent = '양목(陽木)';
    scoreVal.textContent = '84점';
    if (scoreMeterFill) scoreMeterFill.style.width = '84%';
    scoreDesc.textContent = '상생 조화와 성장형 시너지';
    if (harmonyVal) harmonyVal.textContent = '목토생화(木土生火)';
    if (energyVal) energyVal.textContent = '발전과 도약 (吉)';
    if (frequencyVal) frequencyVal.textContent = '87.5 MHz';
    tipText.textContent = '서로에게 긍정적인 자극과 성장을 촉진하는 길한 관계입니다. 장기적인 비전과 공동 프로젝트에서 놀라운 성과를 발휘합니다.';
  } else if (val === '병인') {
    targetLabel.textContent = '병인(丙寅)';
    if (targetElementTag) targetElementTag.textContent = '양화(陽火)';
    scoreVal.textContent = '79점';
    if (scoreMeterFill) scoreMeterFill.style.width = '79%';
    scoreDesc.textContent = '열정적 불꽃과 생명력의 케미';
    if (harmonyVal) harmonyVal.textContent = '화생토(火生土)';
    if (energyVal) energyVal.textContent = '강렬한 매력 (中吉)';
    if (frequencyVal) frequencyVal.textContent = '81.4 MHz';
    tipText.textContent = '첫인상에서 강렬한 매력을 느끼는 조합입니다. 솔직한 감정 교류를 통해 단기적 갈등을 피하고 깊은 신뢰를 쌓을 수 있습니다.';
  } else {
    targetLabel.textContent = '신유(辛酉)';
    if (targetElementTag) targetElementTag.textContent = '음금(陰金)';
    scoreVal.textContent = '55점';
    if (scoreMeterFill) scoreMeterFill.style.width = '55%';
    scoreDesc.textContent = '섬세한 조율이 필요한 관계';
    if (harmonyVal) harmonyVal.textContent = '토생금(土生金)';
    if (energyVal) energyVal.textContent = '거리두기 권장 (平)';
    if (frequencyVal) frequencyVal.textContent = '62.0 MHz';
    tipText.textContent = '서로의 표현 방식과 가치관 차이로 사소한 오해가 생길 수 있습니다. 상대방의 독립적인 성향을 인정하고 거리를 존중할 때 조화를 이룹니다.';
  }
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  updateDailyDopamine();
  updateMatchScore();
});