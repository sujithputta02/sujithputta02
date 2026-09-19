import urllib.request
import json
import os
import re
import xml.etree.ElementTree as ET

PRESS_START_FONT = """@font-face {
  font-family: 'Press Start 2P';
  src: url(data:font/woff2;charset=utf-8;base64,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) format('woff2');
  font-weight: normal;
  font-style: normal;
}"""

def fetch_github_data(username="sujithputta02"):
    """Fetches real user stats, repositories, and commit metrics."""
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'User-Agent': 'Mozilla/5.0'}
    if token:
        headers['Authorization'] = f'token {token}'

    data = {
        'username': username,
        'public_repos': 39,
        'followers': 14,
        'following': 28,
        'stars': 10,
        'forks': 6,
        'commits': 915,
        'prs': 65,
        'issues': 50,
        'contributions': 1600,
        'current_streak': 1,
        'longest_streak': 8,
        'languages': [('TypeScript', 40), ('Python', 26), ('Rust', 12), ('JavaScript', 10), ('HTML/CSS', 12)],
        'featured_repos': []
    }

    try:
        user_url = f"https://api.github.com/users/{username}"
        req = urllib.request.Request(user_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            u_json = json.loads(resp.read().decode('utf-8'))
            data['public_repos'] = u_json.get('public_repos', data['public_repos'])
            data['followers'] = u_json.get('followers', data['followers'])
            data['following'] = u_json.get('following', data['following'])
    except Exception as e:
        print(f"Warning: could not fetch user profile: {e}")

    try:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed"
        req = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read().decode('utf-8'))

        if isinstance(repos, list) and len(repos) > 0:
            data['stars'] = sum(r.get('stargazers_count', 0) for r in repos)
            data['forks'] = sum(r.get('forks_count', 0) for r in repos)

            lang_counts = {}
            for r in repos:
                l = r.get('language')
                if l:
                    lang_counts[l] = lang_counts.get(l, 0) + 1
            total_lang_repos = sum(lang_counts.values()) or 1
            sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
            data['languages'] = [
                (l, round((c / total_lang_repos) * 100)) for l, c in sorted_langs[:5]
            ]

            valid_repos = [
                r for r in repos if not r.get('fork', False) and r.get('name') != username
            ]

            curated_order = ['Esapay', 'DineInGo', 'intentcloud', 'PixelcraftPortfolio', 'wifiauditsec', 'SparkLM']
            repo_map = {r['name']: r for r in valid_repos}

            featured = []
            for name in curated_order:
                if name in repo_map:
                    featured.append(repo_map[name])

            for r in valid_repos:
                if len(featured) >= 4:
                    break
                if r not in featured:
                    featured.append(r)

            data['featured_repos'] = featured[:4]
    except Exception as e:
        print(f"Warning: could not fetch repositories: {e}")

    try:
        commits_url = f"https://api.github.com/search/commits?q=author:{username}"
        c_headers = headers.copy()
        c_headers['Accept'] = 'application/vnd.github.cloak-preview'
        req_c = urllib.request.Request(commits_url, headers=c_headers)
        with urllib.request.urlopen(req_c, timeout=10) as resp:
            c_json = json.loads(resp.read().decode('utf-8'))
            if 'total_count' in c_json and c_json['total_count'] > 0:
                data['commits'] = c_json['total_count']
    except Exception as e:
        print(f"Commits search API notice: {e}")

    try:
        url_prs = f"https://api.github.com/search/issues?q=author:{username}+type:pr"
        req_pr = urllib.request.Request(url_prs, headers=headers)
        with urllib.request.urlopen(req_pr, timeout=10) as resp:
            data['prs'] = json.loads(resp.read().decode('utf-8')).get('total_count', data['prs'])
    except Exception as e:
        print(f"PRs count notice: {e}")

    try:
        url_issues = f"https://api.github.com/search/issues?q=author:{username}+type:issue"
        req_is = urllib.request.Request(url_issues, headers=headers)
        with urllib.request.urlopen(req_is, timeout=10) as resp:
            data['issues'] = json.loads(resp.read().decode('utf-8')).get('total_count', data['issues'])
    except Exception as e:
        print(f"Issues count notice: {e}")

    if not data['featured_repos']:
        data['featured_repos'] = [
            {
                'name': 'Esapay',
                'language': 'Rust',
                'stargazers_count': 2,
                'forks_count': 0,
                'description': 'Policy-bounded multi-agent runtime for adaptive payment infrastructure.',
                'html_url': f'https://github.com/{username}/Esapay'
            },
            {
                'name': 'DineInGo',
                'language': 'TypeScript',
                'stargazers_count': 1,
                'forks_count': 3,
                'description': 'A modern web app for seamless restaurant and event reservations, digital invoicing, and wallet pass delivery.',
                'html_url': f'https://github.com/{username}/DineInGo'
            },
            {
                'name': 'intentcloud',
                'language': 'TypeScript',
                'stargazers_count': 0,
                'forks_count': 0,
                'description': 'An Intent Aware Cognitive Cloud Memory System with real-time semantic context graph.',
                'html_url': f'https://github.com/{username}/intentcloud'
            },
            {
                'name': 'PixelcraftPortfolio',
                'language': 'TypeScript',
                'stargazers_count': 0,
                'forks_count': 0,
                'description': 'Ultra-premium interactive digital showroom showcasing cinematic key art and discomorphic exhibits.',
                'html_url': f'https://github.com/{username}/PixelcraftPortfolio'
            }
        ]

    return data

def escape_xml(text):
    if not text:
        return ""
    return (
        str(text)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&apos;')
    )

def generate_header_svg(stats):
    """
    Generates an upgraded Super Mario Header SVG with:
    - Zero text overlap (crisp pixel drop-shadow filter on clean text)
    - Full gravity simulation: Mario and Goomba walk strictly on ground level (y=200 & y=212, ground top at y=232)
    - Authentic jump physics arc when punching block and clearing Goomba
    - Rolling Super Mario background hills, scalloped bushes, warp pipe with piranha, castle and flagpole
    """
    score_str = f"{stats['commits']:06d}"
    coins_str = f"x{stats['stars']:02d}"
    world_str = f"1-{min(stats['public_repos'], 99)}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 280" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}

      /* HUD Text */
      .hud-label {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #ffffff;
        letter-spacing: 1px;
      }}
      .hud-val {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #fcf800;
        font-weight: bold;
        letter-spacing: 1px;
      }}

      /* Title Text */
      .mario-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 2px;
      }}

      .mario-subtitle {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8.5px;
        fill: #ffffff;
        letter-spacing: 1px;
      }}

      /* Ground Styling */
      .ground-top-strip {{ fill: #fc9838; }}
      .ground-brick-body {{ fill: #b83c18; }}

      /* Question Block and Coin */
      .q-block-box {{
        animation: qBlockBump 12s infinite ease-in-out;
      }}
      .coin-burst {{
        animation: coinBurstPop 12s infinite ease-out;
      }}
      .score-popup {{
        animation: scoreFloat 12s infinite ease-out;
      }}

      /* Mario Gravity Physics and Walk Cycle */
      /* Ground is at y=232. Mario is 32px tall. On-ground y is exactly 200px! */
      .mario-physics {{
        animation: marioRunAndJumpPhysics 12s infinite linear;
      }}

      /* Goomba walks strictly on ground: height=20px, ground y=232 -> y=212px */
      .goomba-walker {{
        animation: goombaPatrol 12s infinite linear;
      }}

      /* Piranha Plant */
      .piranha-anim {{
        animation: piranhaLurking 4s infinite ease-in-out;
      }}

      /* Clouds Parallax */
      .cloud-drift-slow {{ animation: driftClouds 70s infinite linear; }}
      .cloud-drift-fast {{ animation: driftClouds 45s infinite linear -20s; }}

      /* Keyframes */
      @keyframes driftClouds {{
        0% {{ transform: translateX(860px); }}
        100% {{ transform: translateX(-240px); }}
      }}

      @keyframes piranhaLurking {{
        0%, 25% {{ transform: translateY(32px); }}
        40%, 75% {{ transform: translateY(0px); }}
        90%, 100% {{ transform: translateY(32px); }}
      }}

      /* Real Mario Gravity Arc: Ground=200px. Peak Jump=140px. */
      @keyframes marioRunAndJumpPhysics {{
        /* 1. Run right along the ground */
        0% {{ transform: translate(-40px, 200px) scaleX(1); }}
        24% {{ transform: translate(320px, 200px) scaleX(1); }}
        /* 2. Jump up with gravity arc to punch question block at x=375 */
        25% {{ transform: translate(335px, 182px) scaleX(1); }}
        26% {{ transform: translate(355px, 155px) scaleX(1); }}
        27.5% {{ transform: translate(375px, 140px) scaleX(1); }} /* Apex hit */
        29% {{ transform: translate(395px, 162px) scaleX(1); }}
        30% {{ transform: translate(410px, 200px) scaleX(1); }} /* Touchdown */
        /* 3. Run right toward Goomba */
        31% {{ transform: translate(425px, 200px) scaleX(1); }}
        44% {{ transform: translate(525px, 200px) scaleX(1); }}
        /* 4. Jump over Goomba (Apex 145px) */
        45% {{ transform: translate(540px, 180px) scaleX(1); }}
        47% {{ transform: translate(575px, 145px) scaleX(1); }}
        49% {{ transform: translate(610px, 180px) scaleX(1); }}
        50% {{ transform: translate(625px, 200px) scaleX(1); }} /* Touchdown */
        /* 5. Run to Castle Flagpole */
        51% {{ transform: translate(640px, 200px) scaleX(1); }}
        63% {{ transform: translate(750px, 200px) scaleX(1); }}
        /* 6. Wait at flagpole / celebrate */
        66% {{ transform: translate(750px, 200px) scaleX(1); }}
        67% {{ transform: translate(750px, 200px) scaleX(-1); }}
        /* 7. Run back left strictly along the ground */
        68% {{ transform: translate(730px, 200px) scaleX(-1); }}
        98% {{ transform: translate(-40px, 200px) scaleX(-1); }}
        100% {{ transform: translate(-40px, 200px) scaleX(1); }}
      }}

      /* Goomba Patrols strictly on ground y=212 between castle and pipe */
      @keyframes goombaPatrol {{
        0% {{ transform: translate(700px, 212px) scaleX(1); }}
        45% {{ transform: translate(220px, 212px) scaleX(1); }}
        46% {{ transform: translate(220px, 212px) scaleX(-1); }}
        95% {{ transform: translate(700px, 212px) scaleX(-1); }}
        96% {{ transform: translate(700px, 212px) scaleX(1); }}
        100% {{ transform: translate(700px, 212px) scaleX(1); }}
      }}

      /* Block bumps when hit at 27.5% */
      @keyframes qBlockBump {{
        0%, 27% {{ transform: translate(365px, 132px); }}
        27.5% {{ transform: translate(365px, 126px); }}
        28.2% {{ transform: translate(365px, 132px); }}
        100% {{ transform: translate(365px, 132px); }}
      }}

      /* Coin Pops out of block */
      @keyframes coinBurstPop {{
        0%, 27% {{ transform: translate(378px, 130px); opacity: 0; }}
        27.5% {{ opacity: 1; }}
        28.5% {{ transform: translate(378px, 75px) scale(1.3); opacity: 1; }}
        29.5%, 100% {{ transform: translate(378px, 50px); opacity: 0; }}
      }}

      @keyframes scoreFloat {{
        0%, 27.5% {{ transform: translate(370px, 120px); opacity: 0; }}
        28.5% {{ opacity: 1; transform: translate(370px, 68px); }}
        29.8%, 100% {{ opacity: 0; transform: translate(370px, 50px); }}
      }}
    </style>

    <clipPath id="pipe-clip">
      <rect x="0" y="-35" width="56" height="42"/>
    </clipPath>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="280" class="bg-sky"/>

  <!-- Pixel Clouds with Smiling Faces -->
  <g class="cloud-drift-slow" transform="translate(60, 20)">
    <path d="M 30 18 Q 45 0 60 18 Q 75 0 90 18 L 90 32 L 30 32 Z" fill="#ffffff" opacity="0.9"/>
    <ellipse cx="60" cy="22" rx="30" ry="12" fill="#ffffff"/>
    <rect x="52" y="16" width="2" height="6" fill="#000000" opacity="0.4"/>
    <rect x="66" y="16" width="2" height="6" fill="#000000" opacity="0.4"/>
  </g>
  <g class="cloud-drift-fast" transform="translate(480, 35)">
    <path d="M 20 12 Q 32 0 45 12 Q 58 0 70 12 L 70 24 L 20 24 Z" fill="#ffffff" opacity="0.8"/>
    <ellipse cx="45" cy="16" rx="25" ry="9" fill="#ffffff"/>
  </g>

  <!-- Rolling Green Hills in Background (Classic 1-1 World) -->
  <g transform="translate(0, 0)">
    <!-- Big Green Hill Left -->
    <path d="M -20 232 C 40 160, 100 160, 160 232 Z" fill="#00a800" stroke="#000000" stroke-width="2"/>
    <path d="M 20 232 C 55 180, 85 180, 120 232 Z" fill="#008000"/>
    <circle cx="70" cy="182" r="3" fill="#fcf800"/>
    <circle cx="70" cy="182" r="1.5" fill="#000000"/>

    <!-- Rolling Green Hill Right -->
    <path d="M 640 232 C 700 165, 750 165, 810 232 Z" fill="#00a800" stroke="#000000" stroke-width="2"/>
    <path d="M 675 232 C 715 185, 745 185, 785 232 Z" fill="#008000"/>
    <circle cx="730" cy="185" r="3" fill="#fcf800"/>
    <circle cx="730" cy="185" r="1.5" fill="#000000"/>

    <!-- Scalloped Bushes near Pipe -->
    <g transform="translate(60, 208)">
      <circle cx="12" cy="16" r="12" fill="#00a800" stroke="#000" stroke-width="1.5"/>
      <circle cx="28" cy="12" r="14" fill="#00f800" stroke="#000" stroke-width="1.5"/>
      <circle cx="44" cy="16" r="12" fill="#00a800" stroke="#000" stroke-width="1.5"/>
      <rect x="0" y="16" width="56" height="8" fill="#00a800"/>
    </g>
  </g>

  <!-- TOP HUD BAR (Iconic NES Arcade) -->
  <g transform="translate(45, 20)">
    <text x="0" y="0" class="hud-label">MARIO / SUJITH</text>
    <text x="0" y="16" class="hud-val">{score_str}</text>

    <!-- Gold Coin Icon in HUD -->
    <g transform="translate(230, -6)">
      <ellipse cx="6" cy="12" rx="4" ry="7" fill="#fcf800" stroke="#000000" stroke-width="1"/>
      <line x1="6" y1="8" x2="6" y2="16" stroke="#fc9838" stroke-width="1"/>
    </g>
    <text x="245" y="0" class="hud-label">COINS</text>
    <text x="245" y="16" class="hud-val">{coins_str}</text>

    <text x="470" y="0" class="hud-label">WORLD</text>
    <text x="470" y="16" class="hud-val">{world_str}</text>

    <text x="660" y="0" class="hud-label">TIME</text>
    <text x="660" y="16" class="hud-val">2026</text>
  </g>

  <!-- TITLE: SUJITH PUTTA (CLEAN VIBRANT LETTERS, ZERO SHADOW, NO BLACK LAYER) -->
  <g transform="translate(425, 78)">
    <text x="0" y="0" class="mario-title" text-anchor="middle">
      <tspan fill="#e52521">S</tspan><tspan fill="#f2a900">U</tspan><tspan fill="#002fbe">J</tspan><tspan fill="#43b047">I</tspan><tspan fill="#e52521">T</tspan><tspan fill="#f2a900">H</tspan>
      <tspan fill="#ffffff"> </tspan>
      <tspan fill="#002fbe">P</tspan><tspan fill="#43b047">U</tspan><tspan fill="#e52521">T</tspan><tspan fill="#f2a900">T</tspan><tspan fill="#002fbe">A</tspan>
    </text>
  </g>

  <!-- SUBTITLE CARTRIDGE BANNER (Properly spaced above bricks!) -->
  <g transform="translate(195, 96)">
    <rect width="460" height="22" rx="4" fill="#000000" stroke="#fc9838" stroke-width="2"/>
    <text x="230" y="15" class="mario-subtitle" text-anchor="middle">> FULL-STACK DEVELOPER &amp; AI SPECIALIST &lt;</text>
  </g>

  <!-- FLOATING BRICKS & QUESTION BLOCK -->
  <!-- Left Brick -->
  <g transform="translate(335, 132)">
    <rect width="30" height="30" fill="#b83c18" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="10" x2="30" y2="10" stroke="#000000" stroke-width="1.5"/>
    <line x1="0" y1="20" x2="30" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="15" y1="0" x2="15" y2="10" stroke="#000000" stroke-width="1.5"/>
    <line x1="7" y1="10" x2="7" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="22" y1="10" x2="22" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="15" y1="20" x2="15" y2="30" stroke="#000000" stroke-width="1.5"/>
  </g>

  <!-- Bumping Question Block -->
  <g class="q-block-box">
    <rect width="30" height="30" fill="#fc9838" stroke="#000000" stroke-width="2"/>
    <text x="15" y="21" font-family="'Press Start 2P', monospace" font-size="12" fill="#ffffff" font-weight="bold" text-anchor="middle">?</text>
    <circle cx="4" cy="4" r="1" fill="#000000"/>
    <circle cx="26" cy="4" r="1" fill="#000000"/>
    <circle cx="4" cy="26" r="1" fill="#000000"/>
    <circle cx="26" cy="26" r="1" fill="#000000"/>
  </g>

  <!-- Right Brick -->
  <g transform="translate(395, 132)">
    <rect width="30" height="30" fill="#b83c18" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="10" x2="30" y2="10" stroke="#000000" stroke-width="1.5"/>
    <line x1="0" y1="20" x2="30" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="15" y1="0" x2="15" y2="10" stroke="#000000" stroke-width="1.5"/>
    <line x1="7" y1="10" x2="7" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="22" y1="10" x2="22" y2="20" stroke="#000000" stroke-width="1.5"/>
    <line x1="15" y1="20" x2="15" y2="30" stroke="#000000" stroke-width="1.5"/>
  </g>

  <!-- POPPING COIN & SCORE -->
  <g class="coin-burst">
    <ellipse cx="6" cy="10" rx="5" ry="8" fill="#fcf800" stroke="#000000" stroke-width="1.5"/>
    <line x1="6" y1="5" x2="6" y2="15" stroke="#fc9838" stroke-width="1.5"/>
  </g>
  <g class="score-popup">
    <text x="0" y="0" font-family="'Press Start 2P', monospace" font-size="8" fill="#ffffff" stroke="#000" stroke-width="1.5" paint-order="stroke fill" font-weight="bold">+200</text>
  </g>

  <!-- GREEN WARP PIPE (Grounded firmly at y=232) -->
  <g transform="translate(140, 172)">
    <!-- Piranha Plant clipped inside pipe -->
    <g clip-path="url(#pipe-clip)">
      <g class="piranha-anim" transform="translate(11, 0)">
        <rect x="10" y="8" width="6" height="24" fill="#00a800" stroke="#000" stroke-width="1"/>
        <path d="M 6 18 Q 0 16 2 12 Q 8 14 10 18 Z" fill="#00a800"/>
        <path d="M 16 18 Q 24 16 22 12 Q 16 14 14 18 Z" fill="#00a800"/>
        <path d="M 3 8 C 3 -4, 23 -4, 23 8 Z" fill="#e52521" stroke="#000" stroke-width="1.5"/>
        <circle cx="8" cy="2" r="1.5" fill="#ffffff"/>
        <circle cx="16" cy="0" r="1.5" fill="#ffffff"/>
        <circle cx="19" cy="4" r="1.5" fill="#ffffff"/>
        <polygon points="5,8 7,5 9,8 11,5 13,8 15,5 17,8 19,5 21,8" fill="#ffffff"/>
      </g>
    </g>
    <!-- Pipe Collar -->
    <rect x="0" y="6" width="52" height="18" fill="#00f800" stroke="#000000" stroke-width="2"/>
    <rect x="4" y="8" width="6" height="14" fill="#ffffff" opacity="0.8"/>
    <!-- Pipe Stem resting directly on ground (y=232) -->
    <rect x="4" y="24" width="44" height="36" fill="#00a800" stroke="#000000" stroke-width="2"/>
    <rect x="8" y="24" width="6" height="36" fill="#00f800"/>
  </g>

  <!-- PEACH'S CASTLE & FLAGPOLE (Right end level goal) -->
  <g transform="translate(760, 132)">
    <!-- Flagpole (Touches ground at y=100 from transform) -->
    <line x1="0" y1="0" x2="0" y2="100" stroke="#000000" stroke-width="3"/>
    <circle cx="0" cy="0" r="4" fill="#00f800" stroke="#000" stroke-width="1.5"/>
    <polygon points="0,6 24,14 0,22" fill="#e52521" stroke="#000" stroke-width="1.5"/>
    <!-- Castle -->
    <g transform="translate(22, 28)">
      <rect x="0" y="20" width="46" height="52" fill="#b83c18" stroke="#000000" stroke-width="2"/>
      <rect x="4" y="2" width="10" height="18" fill="#b83c18" stroke="#000000" stroke-width="1.5"/>
      <rect x="18" y="2" width="10" height="18" fill="#b83c18" stroke="#000000" stroke-width="1.5"/>
      <rect x="32" y="2" width="10" height="18" fill="#b83c18" stroke="#000000" stroke-width="1.5"/>
      <path d="M 16 72 C 16 52, 30 52, 30 72 Z" fill="#000000"/>
    </g>
  </g>

  <!-- GOOMBA MINION (WALKS FIRMLY ON GROUND y=232) -->
  <!-- Goomba height is 20px, anchored at 212px -->
  <g class="goomba-walker">
    <path d="M 3 14 C 3 2, 21 2, 21 14 Z" fill="#a85400" stroke="#000000" stroke-width="1.5"/>
    <path d="M 7 14 L 17 14 L 17 18 L 7 18 Z" fill="#fce4a0" stroke="#000000" stroke-width="1"/>
    <ellipse cx="6" cy="18" rx="4" ry="2.5" fill="#000000"/>
    <ellipse cx="18" cy="18" rx="4" ry="2.5" fill="#000000"/>
    <!-- Eyes -->
    <rect x="8" y="7" width="2" height="4" fill="#000000"/>
    <rect x="14" y="7" width="2" height="4" fill="#000000"/>
    <!-- Angry Eyebrows -->
    <line x1="7" y1="5" x2="10" y2="7" stroke="#000000" stroke-width="1.5"/>
    <line x1="17" y1="5" x2="14" y2="7" stroke="#000000" stroke-width="1.5"/>
  </g>

  <!-- MARIO HERO CHARACTER (WALKS FIRMLY ON GROUND y=232) -->
  <!-- Mario height is 32px, anchored at 200px so shoes touch y=232! -->
  <g class="mario-physics">
    <!-- Cap -->
    <path d="M 6 0 h 14 v 4 h -14 Z" fill="#ff0000"/>
    <path d="M 4 2 h 20 v 3 h -20 Z" fill="#ff0000"/>
    <!-- Face / Hair / Mustache -->
    <path d="M 6 5 h 6 v 3 h -6 Z" fill="#6b3300"/>
    <path d="M 12 5 h 6 v 3 h -6 Z" fill="#ffcca0"/>
    <rect x="18" y="5" width="2" height="4" fill="#000000"/>
    <path d="M 6 8 h 2 v 4 h -2 Z" fill="#6b3300"/>
    <path d="M 8 8 h 12 v 6 h -12 Z" fill="#ffcca0"/>
    <path d="M 14 11 h 8 v 3 h -8 Z" fill="#6b3300"/>
    <!-- Overalls & Shirt -->
    <path d="M 4 14 h 18 v 10 h -18 Z" fill="#ff0000"/>
    <path d="M 8 14 h 9 v 12 h -9 Z" fill="#0000d8"/>
    <!-- Yellow Buttons -->
    <circle cx="10" cy="19" r="1.5" fill="#fcf800"/>
    <circle cx="15" cy="19" r="1.5" fill="#fcf800"/>
    <!-- Hands -->
    <circle cx="2" cy="18" r="3" fill="#ffcca0" stroke="#000000" stroke-width="1"/>
    <circle cx="23" cy="18" r="3" fill="#ffcca0" stroke="#000000" stroke-width="1"/>
    <!-- Boots touching ground -->
    <rect x="5" y="26" width="6" height="6" fill="#6b3300" stroke="#000000" stroke-width="1"/>
    <rect x="14" y="26" width="6" height="6" fill="#6b3300" stroke="#000000" stroke-width="1"/>
  </g>

  <!-- GROUND TERRAIN (Top edge is exactly at y=232) -->
  <g transform="translate(0, 232)">
    <!-- Top Orange/Grass Strip (6px) -->
    <rect width="850" height="6" class="ground-top-strip"/>
    <!-- Brick Soil Block Body (42px) -->
    <rect y="6" width="850" height="42" class="ground-brick-body"/>
    <!-- Classic Mario Brick Grid lines -->
    <path d="M 0 6 L 850 6 M 0 16 L 850 16 M 0 26 L 850 26 M 0 36 L 850 36 M 0 46 L 850 46" stroke="#000000" stroke-width="1" stroke-opacity="0.4"/>
    {" ".join(f'<path d="M {x} 6 v 42" stroke="#000000" stroke-width="1" stroke-opacity="0.4"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def generate_retro_stats_svg(stats):
    """
    Generates upgraded Mario Bros Status Board with Question Block corner rivets,
    segmented glowing power bars, and authentic Mario power-up items.
    """
    powerup_icons = [
        # Fire Flower (Python)
        """<g class="powerup-icon"><circle cx="10" cy="10" r="9" fill="#ff3000" stroke="#000" stroke-width="1.5"/><circle cx="10" cy="10" r="5.5" fill="#fc9838"/><circle cx="10" cy="10" r="2.5" fill="#fcf800"/></g>""",
        # Cape Feather (TypeScript)
        """<g class="powerup-icon"><path d="M 3 17 L 17 3 L 13 17 Z" fill="#00f0ff" stroke="#000" stroke-width="1.5"/><circle cx="9" cy="10" r="1.5" fill="#ffffff"/></g>""",
        # Super Mushroom (Rust)
        """<g class="powerup-icon"><path d="M 3 10 C 3 2, 17 2, 17 10 Z" fill="#ff0000" stroke="#000" stroke-width="1.5"/><circle cx="7" cy="6" r="2" fill="#ffffff"/><circle cx="13" cy="6" r="2" fill="#ffffff"/><rect x="7" y="10" width="6" height="6" fill="#fce4a0" stroke="#000" stroke-width="1.5"/></g>""",
        # Super Star (AI / RAG)
        """<g class="powerup-icon"><polygon points="10,2 12.5,7.5 18,7.5 13.5,11.5 15.5,17 10,13.5 4.5,17 6.5,11.5 2,7.5 7.5,7.5" fill="#fcf800" stroke="#000" stroke-width="1.5"/><circle cx="8" cy="8.5" r="1" fill="#000"/><circle cx="12" cy="8.5" r="1" fill="#000"/></g>"""
    ]

    langs = stats.get('languages', [('TypeScript', 40), ('Python', 26), ('Rust', 12), ('JavaScript', 10)])
    while len(langs) < 4:
        langs.append(('FullStack', 10))

    powerup_rows = []
    y_offsets = [50, 92, 134, 176]
    for i in range(4):
        lang_name, pct = langs[i]
        icon = powerup_icons[i % len(powerup_icons)]
        y = y_offsets[i]
        bar_w = max(18, min(80, int(pct * 1.5)))
        lvl = min(99, 70 + pct // 2)
        powerup_rows.append(f"""
    <!-- Skill {i+1}: {lang_name} -->
    <g transform="translate(18, {y})">
      {icon}
      <text x="28" y="12" class="text-label">{escape_xml(lang_name).upper()}:</text>
      <!-- Segmented Level Meter -->
      <g transform="translate(165, 3)">
        <rect width="82" height="11" rx="2" fill="#111111" stroke="#000000" stroke-width="1.5"/>
        <rect width="{bar_w}" height="7" x="2" y="2" rx="1" fill="#00a800" class="bar-glow"/>
      </g>
      <text x="260" y="12" class="text-val">LV.{lvl}</text>
    </g>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 340" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}
      .cloud {{ fill: #ffffff; }}

      .text-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 13px;
        fill: #ffffff;
        stroke: #000000;
        stroke-width: 2.5;
        paint-order: stroke fill;
      }}
      .text-panel-header {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #b83c18;
        font-weight: bold;
      }}
      .text-label {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #4a3728;
        font-weight: bold;
      }}
      .text-val {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #008800;
        font-weight: bold;
      }}
      .text-rank {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #e52521;
        font-weight: bold;
      }}

      /* Mario Dialogue Board with Beveled Border */
      .box-container {{
        fill: #fce4a0;
        stroke: #000000;
        stroke-width: 3.5;
      }}
      .box-inner {{
        fill: none;
        stroke: #b83c18;
        stroke-width: 1.5;
      }}

      .powerup-icon {{
        animation: bouncePowerup 2s infinite ease-in-out;
      }}
      .bar-glow {{
        animation: barGlowPulse 2.5s infinite ease-in-out;
      }}

      @keyframes bouncePowerup {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-3px); }}
      }}

      @keyframes barGlowPulse {{
        0%, 100% {{ fill: #00a800; }}
        50% {{ fill: #00f800; }}
      }}

      .cloud-bg-1 {{ animation: cloudDrift 60s infinite linear; }}
      .cloud-bg-2 {{ animation: cloudDrift 90s infinite linear -30s; }}

      @keyframes cloudDrift {{
        0% {{ transform: translateX(850px); }}
        100% {{ transform: translateX(-200px); }}
      }}
    </style>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="340" class="bg-sky"/>

  <!-- Clouds -->
  <g class="cloud-bg-1" transform="translate(100, 10)">
    <path d="M120,20 C110,20 100,28 100,38 C90,38 80,46 80,56 C80,66 90,74 100,74 L160,74 C170,74 180,66 180,56 C180,46 170,38 160,38 C160,28 150,20 140,20 Z" class="cloud" opacity="0.6"/>
  </g>
  <g class="cloud-bg-2" transform="translate(500, 20)">
    <path d="M60,10 C55,10 50,14 50,19 C45,19 40,23 40,28 C40,33 45,37 50,37 L80,37 C85,37 90,33 90,28 C90,23 85,19 80,19 C80,14 75,10 70,10 Z" class="cloud" opacity="0.5"/>
  </g>

  <!-- Title -->
  <text x="425" y="32" class="text-title" text-anchor="middle">> HERO METRICS &amp; REAL-TIME POWER-UPS &lt;</text>

  <!-- PANEL 1: HERO METRICS -->
  <g transform="translate(40, 50)">
    <rect width="365" height="230" rx="8" class="box-container"/>
    <rect x="6" y="6" width="353" height="218" rx="5" class="box-inner"/>
    <!-- Question Block Rivets on Corners -->
    <rect x="8" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="347" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="8" y="212" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="347" y="212" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>

    <text x="24" y="30" class="text-panel-header">> HERO METRICS</text>

    <!-- Commits -->
    <g transform="translate(24, 50)" class="powerup-icon">
      <path d="M3 8 C3 2, 13 2, 13 8 Z" fill="#a85400" stroke="#000" stroke-width="1"/>
      <rect x="5" y="8" width="6" height="3" fill="#fce4a0"/>
    </g>
    <text x="50" y="58" class="text-label">COMMITS STOMPED:</text>
    <text x="245" y="58" class="text-val" id="val-commits">{stats['commits']}</text>

    <!-- Coins -->
    <g transform="translate(24, 90)" class="powerup-icon">
      <ellipse cx="8" cy="8" rx="4" ry="7" fill="#fcf800" stroke="#000" stroke-width="1"/>
      <line x1="8" y1="4" x2="8" y2="12" stroke="#fc9838" stroke-width="1"/>
    </g>
    <text x="50" y="98" class="text-label">COINS COLLECTED:</text>
    <text x="245" y="98" class="text-val" id="val-stars">{stats['stars']}</text>

    <!-- Levels Cleared -->
    <g transform="translate(24, 130)" class="powerup-icon">
      <rect x="3" y="1" width="10" height="13" fill="#00a800" stroke="#000" stroke-width="1"/>
      <rect x="1" y="1" width="14" height="4" fill="#00f800" stroke="#000" stroke-width="1"/>
    </g>
    <text x="50" y="138" class="text-label">LEVELS CLEARED:</text>
    <text x="245" y="138" class="text-val" id="val-repos">{stats['public_repos']}</text>

    <!-- Allies -->
    <g transform="translate(24, 170)" class="powerup-icon">
      <circle cx="8" cy="6" r="6" fill="#ff0000" stroke="#000" stroke-width="1"/>
      <circle cx="8" cy="11" r="4" fill="#ffcca0" stroke="#000" stroke-width="1"/>
    </g>
    <text x="50" y="178" class="text-label">PARTY ALLIES (NPC):</text>
    <text x="245" y="178" class="text-val" id="val-followers">{stats['followers']}</text>

    <!-- Rank Status -->
    <text x="50" y="210" class="text-label">ADVENTURER RANK:</text>
    <text x="245" y="210" class="text-rank">S-RANK ARCHITECT</text>
  </g>

  <!-- PANEL 2: POWER-UPS -->
  <g transform="translate(445, 50)">
    <rect width="365" height="230" rx="8" class="box-container"/>
    <rect x="6" y="6" width="353" height="218" rx="5" class="box-inner"/>
    <rect x="8" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="347" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="8" y="212" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="347" y="212" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>

    <text x="24" y="30" class="text-panel-header">> POWER-UP ABILITIES</text>
    {"".join(powerup_rows)}
  </g>

  <!-- Ground -->
  <g transform="translate(0, 315)">
    <rect width="850" height="5" fill="#fc9838"/>
    <rect y="5" width="850" height="20" fill="#b83c18"/>
    <path d="M 0 5 L 850 5 M 0 12 L 850 12" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>
    {" ".join(f'<path d="M {x} 0 v 25" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def generate_adventure_quests_svg(stats):
    """Generates the master Adventure Quests board with real repositories and live stats."""
    repos = stats.get('featured_repos', [])

    difficulties = ['BOSS STAGE', 'ELITE QUEST', 'SPECIAL QUEST', 'MAIN QUEST']
    colors = ['#e52521', '#fc9838', '#002fbe', '#00a800']
    points = ['+9900 PTS', '+7500 PTS', '+6000 PTS', '+5000 PTS']

    cards = []
    y_start = 50
    card_h = 70
    card_gap = 9

    for i in range(min(4, len(repos))):
        r = repos[i]
        name = r.get('name', f'Quest-{i+1}')
        lang = r.get('language') or 'Multi-Stack'
        stars = r.get('stargazers_count', 0)
        forks = r.get('forks_count', 0)
        desc = r.get('description') or 'High performance autonomous system engineering.'
        if len(desc) > 82:
            desc = desc[:79] + '...'

        diff = difficulties[i % len(difficulties)]
        diff_color = colors[i % len(colors)]
        pts = points[i % len(points)]
        stage_num = f"LV 1-{i+1}"
        y = y_start + i * (card_h + card_gap)

        card = f"""
  <!-- QUEST {i+1}: {escape_xml(name)} -->
  <g transform="translate(0, {y})">
    <rect x="35" y="0" width="780" height="{card_h}" rx="8" class="quest-card-bg"/>
    <rect x="41" y="5" width="768" height="{card_h - 10}" rx="5" class="quest-card-inner"/>

    <!-- Level Stage Badge -->
    <rect x="52" y="11" width="75" height="18" rx="3" class="badge-level"/>
    <text x="89" y="24" class="badge-text" text-anchor="middle">{stage_num}</text>

    <!-- Quest / Repo Name -->
    <text x="138" y="24" class="text-quest-title">{escape_xml(name)}</text>

    <!-- Language Tag -->
    <rect x="350" y="11" width="105" height="18" rx="3" fill="#222222" stroke="#000" stroke-width="1"/>
    <text x="402" y="24" font-family="'Press Start 2P', monospace" font-size="7" fill="#fcf800" text-anchor="middle">👾 {escape_xml(lang)}</text>

    <!-- Difficulty -->
    <text x="475" y="24" class="text-meta-label">DIFF:<tspan fill="{diff_color}"> {diff}</tspan></text>

    <!-- Stars & Forks Stats -->
    <text x="635" y="24" font-family="'Press Start 2P', monospace" font-size="7.5" fill="#000000">⭐{stars} 🍴{forks}</text>

    <!-- Reward Points Badge -->
    <g transform="translate(715, 11)">
      <ellipse cx="6" cy="9" rx="4" ry="6" class="coin-gold"/>
      <text x="14" y="12" class="text-meta-label" fill="#b83c18">{pts}</text>
    </g>

    <!-- Quest Objective -->
    <text x="52" y="48" class="text-desc">> OBJ: {escape_xml(desc)}</text>
  </g>"""
        cards.append(card)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 375" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}
      .cloud {{ fill: #ffffff; }}

      .text-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 13px;
        fill: #ffffff;
        stroke: #000000;
        stroke-width: 2.5;
        paint-order: stroke fill;
      }}

      .quest-card-bg {{
        fill: #fce4a0;
        stroke: #000000;
        stroke-width: 3;
      }}
      .quest-card-inner {{
        fill: none;
        stroke: #b83c18;
        stroke-width: 1.5;
      }}

      .text-quest-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 9.5px;
        fill: #000000;
        font-weight: bold;
      }}
      .text-meta-label {{
        font-family: 'Press Start 2P', monospace;
        font-size: 7.5px;
        fill: #b83c18;
        font-weight: bold;
      }}
      .text-desc {{
        font-family: 'Press Start 2P', monospace;
        font-size: 7.5px;
        fill: #4a3728;
      }}

      .badge-level {{
        fill: #fc9838;
        stroke: #000000;
        stroke-width: 1.5;
      }}
      .badge-text {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #000000;
        font-weight: bold;
      }}

      .coin-gold {{ fill: #fcf800; stroke: #000000; stroke-width: 1; }}

      .cloud-bg-1 {{ animation: cloudDrift 60s infinite linear; }}
      .cloud-bg-2 {{ animation: cloudDrift 90s infinite linear -45s; }}

      @keyframes cloudDrift {{
        0% {{ transform: translateX(850px); }}
        100% {{ transform: translateX(-200px); }}
      }}
    </style>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="375" class="bg-sky"/>

  <!-- Clouds Background -->
  <g class="cloud-bg-1" transform="translate(50, 10)">
    <path d="M120,20 C110,20 100,28 100,38 C90,38 80,46 80,56 C80,66 90,74 100,74 L160,74 C170,74 180,66 180,56 C180,46 170,38 160,38 C160,28 150,20 140,20 Z" class="cloud" opacity="0.6"/>
  </g>
  <g class="cloud-bg-2" transform="translate(600, 15)">
    <path d="M60,10 C55,10 50,14 50,19 C45,19 40,23 40,28 C40,33 45,37 50,37 L80,37 C85,37 90,33 90,28 C90,23 85,19 80,19 C80,14 75,10 70,10 Z" class="cloud" opacity="0.5"/>
  </g>

  <!-- Screen Title -->
  <text x="425" y="32" class="text-title" text-anchor="middle">> REAL-TIME ADVENTURE QUESTS &lt;</text>

  <!-- Dynamic Quest Cards -->
  {"".join(cards)}

  <!-- Ground -->
  <g transform="translate(0, 355)">
    <rect width="850" height="5" fill="#fc9838"/>
    <rect y="5" width="850" height="15" fill="#b83c18"/>
    <path d="M 0 5 L 850 5 M 0 12 L 850 12" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>
    {" ".join(f'<path d="M {x} 0 v 20" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def generate_individual_quest_card(repo, stage_idx):
    """Generates an individual, responsive clickable cartridge SVG for a specific repo."""
    name = repo.get('name', f'Stage-{stage_idx}')
    lang = repo.get('language') or 'Multi-Stack'
    stars = repo.get('stargazers_count', 0)
    forks = repo.get('forks_count', 0)
    desc = repo.get('description') or 'High performance autonomous system engineering.'
    if len(desc) > 65:
        desc = desc[:62] + '...'

    stage_titles = ['BOSS LEVEL', 'ELITE LEVEL', 'SPECIAL STAGE', 'ADVENTURE STAGE']
    colors = ['#e52521', '#fc9838', '#002fbe', '#00a800']
    diff_color = colors[(stage_idx - 1) % len(colors)]
    badge_label = f"STAGE 1-{stage_idx}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 140" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}
      .card-bg {{ fill: #fce4a0; stroke: #000000; stroke-width: 3; rx: 8; }}
      .card-inner {{ fill: none; stroke: #b83c18; stroke-width: 1.5; rx: 5; }}
      .stage-badge {{ fill: {diff_color}; stroke: #000000; stroke-width: 1.5; rx: 3; }}
      .stage-text {{ font-family: 'Press Start 2P', monospace; font-size: 7.5px; fill: #ffffff; font-weight: bold; }}
      .repo-title {{ font-family: 'Press Start 2P', monospace; font-size: 9.5px; fill: #000000; font-weight: bold; }}
      .repo-desc {{ font-family: 'Press Start 2P', monospace; font-size: 7px; fill: #4a3728; }}
      .meta-text {{ font-family: 'Press Start 2P', monospace; font-size: 7px; fill: #b83c18; font-weight: bold; }}
      .action-pill {{ fill: #00a800; stroke: #000000; stroke-width: 1; rx: 3; animation: pulsePlay 2s infinite ease-in-out; }}
      @keyframes pulsePlay {{
        0%, 100% {{ fill: #00a800; }}
        50% {{ fill: #00f800; }}
      }}
    </style>
  </defs>

  <!-- Base Cartridge -->
  <rect x="4" y="4" width="412" height="132" class="card-bg"/>
  <rect x="9" y="9" width="402" height="122" class="card-inner"/>

  <!-- Stage Badge -->
  <rect x="18" y="16" width="80" height="18" class="stage-badge"/>
  <text x="58" y="28" class="stage-text" text-anchor="middle">{badge_label}</text>

  <!-- Repo Title -->
  <text x="110" y="28" class="repo-title">{escape_xml(name)}</text>

  <!-- Stats & Lang -->
  <g transform="translate(18, 44)">
    <rect width="80" height="16" rx="3" fill="#222222" stroke="#000" stroke-width="1"/>
    <text x="40" y="11" font-family="'Press Start 2P', monospace" font-size="6.5" fill="#fcf800" text-anchor="middle">👾 {escape_xml(lang)}</text>
    <text x="95" y="12" class="meta-text">⭐ {stars}  🍴 {forks}</text>
  </g>

  <!-- Objective Description -->
  <text x="18" y="78" class="repo-desc">> OBJ: {escape_xml(desc)}</text>

  <!-- Launch Stage Interactive CTA -->
  <g transform="translate(18, 96)">
    <rect width="140" height="20" class="action-pill"/>
    <text x="70" y="14" font-family="'Press Start 2P', monospace" font-size="7" fill="#ffffff" text-anchor="middle">▶ PLAY STAGE / REPO</text>
  </g>
</svg>"""
    return svg

def generate_system_overview_svg(stats):
    """Generates the System Overview SVG with live specs and uptime."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}
      .cloud {{ fill: #ffffff; }}

      .dialogue-box {{
        fill: #fce4a0;
        stroke: #000000;
        stroke-width: 4;
      }}
      .dialogue-inner {{
        fill: none;
        stroke: #b83c18;
        stroke-width: 2;
      }}

      .text-prompt {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #b83c18;
      }}
      .text-label {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #b83c18;
        font-weight: bold;
      }}
      .text-val {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #000000;
      }}
      .text-val-green {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #008800;
        font-weight: bold;
      }}

      /* NES Controller Graphics */
      .ctrl-body {{ fill: #cccccc; stroke: #000000; stroke-width: 2; }}
      .ctrl-dark-rect {{ fill: #3e3e3e; }}
      .ctrl-button-red {{ fill: #e52521; stroke: #000000; stroke-width: 1.5; }}
      .ctrl-dpad {{ fill: #000000; }}
      .ctrl-label {{ font-family: 'Press Start 2P', monospace; font-size: 5px; fill: #e52521; }}
      .ctrl-action-pill {{ fill: #3e3e3e; }}

      .cloud-bg-1 {{ animation: cloudDrift 50s infinite linear; }}
      .cloud-bg-2 {{ animation: cloudDrift 80s infinite linear -20s; }}

      @keyframes cloudDrift {{
        0% {{ transform: translateX(850px); }}
        100% {{ transform: translateX(-200px); }}
      }}
    </style>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="360" class="bg-sky"/>

  <!-- Clouds -->
  <g class="cloud-bg-1" transform="translate(100, 10)">
    <path d="M120,20 C110,20 100,28 100,38 C90,38 80,46 80,56 C80,66 90,74 100,74 L160,74 C170,74 180,66 180,56 C180,46 170,38 160,38 C160,28 150,20 140,20 Z" class="cloud" opacity="0.6"/>
  </g>
  <g class="cloud-bg-2" transform="translate(450, 20)">
    <path d="M60,10 C55,10 50,14 50,19 C45,19 40,23 40,28 C40,33 45,37 50,37 L80,37 C85,37 90,33 90,28 C90,23 85,19 80,19 C80,14 75,10 70,10 Z" class="cloud" opacity="0.5"/>
  </g>

  <!-- Main Dialogue Box -->
  <rect x="35" y="30" width="780" height="280" rx="12" class="dialogue-box"/>
  <rect x="42" y="37" width="766" height="266" rx="8" class="dialogue-inner"/>

  <!-- LEFT: NES Controller -->
  <g transform="translate(65, 125)">
    <rect width="130" height="70" rx="8" class="ctrl-body"/>
    <rect x="10" y="10" width="110" height="50" rx="4" class="ctrl-dark-rect"/>
    <circle cx="90" cy="38" r="8" class="ctrl-button-red"/>
    <text x="90" y="55" class="ctrl-label" text-anchor="middle">B</text>
    <circle cx="110" cy="38" r="8" class="ctrl-button-red"/>
    <text x="110" y="55" class="ctrl-label" text-anchor="middle">A</text>
    <!-- D-Pad -->
    <path d="M 22 28 h 10 v 10 h -10 z" class="ctrl-dpad"/>
    <path d="M 27 23 h 10 v 10 h -10 z" class="ctrl-dpad"/>
    <path d="M 32 28 h 10 v 10 h -10 z" class="ctrl-dpad"/>
    <path d="M 27 33 h 10 v 10 h -10 z" class="ctrl-dpad"/>
    <circle cx="32" cy="33" r="2" fill="#3e3e3e"/>
    <rect x="52" y="35" width="12" height="4" rx="2" class="ctrl-action-pill"/>
    <rect x="68" y="35" width="12" height="4" rx="2" class="ctrl-action-pill"/>
    <text x="58" y="46" font-family="'Press Start 2P'" font-size="4" fill="#ffffff" text-anchor="middle">SELECT</text>
    <text x="74" y="46" font-family="'Press Start 2P'" font-size="4" fill="#ffffff" text-anchor="middle">START</text>
  </g>

  <!-- RIGHT: Terminal Output -->
  <g transform="translate(230, 50)">
    <text x="10" y="15" class="text-prompt">sujithputta02@terminal:~$ ./retro_boot.sh --status</text>

    <g transform="translate(10, 42)">
      <text x="0" y="0" class="text-label">OS:<tspan class="text-val"> NES / Pixel Kingdom OS 64-Bit</tspan></text>
      <text x="0" y="20" class="text-label">Host:<tspan class="text-val"> Developer &amp; AI Specialist</tspan></text>
      <text x="0" y="40" class="text-label">Kernel:<tspan class="text-val"> Retro Game Engine v2.0 (Real-Time Sync)</tspan></text>
      <text x="0" y="60" class="text-label">Uptime:<tspan class="text-val"> {stats['public_repos']} Repos Cleared 🌟 ({stats['stars']} Coins)</tspan></text>
      <text x="0" y="80" class="text-label">Shell:<tspan class="text-val"> Rust / TypeScript / Python</tspan></text>
      <text x="0" y="100" class="text-label">Resolution:<tspan class="text-val"> 8-Bit Pixel Art Responsive UI</tspan></text>
      <text x="0" y="120" class="text-label">Editor:<tspan class="text-val"> VS Code / Cursor / NeoVim</tspan></text>
      <text x="0" y="140" class="text-label">CPU:<tspan class="text-val"> Ricoh 2A03 (Multi-Agent Neural Core)</tspan></text>
      <text x="0" y="160" class="text-label">Memory:<tspan class="text-val"> High-Performance Distributed RAM</tspan></text>
      <text x="0" y="180" class="text-label">Mission:<tspan class="text-val-green"> Defeating bugs &amp; architecting high-yield AI systems</tspan></text>
    </g>
  </g>

  <!-- Ground Blocks -->
  <g transform="translate(0, 335)">
    <rect width="850" height="5" fill="#fc9838"/>
    <rect y="5" width="850" height="20" fill="#b83c18"/>
    <path d="M 0 5 L 850 5 M 0 12 L 850 12" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>
    {" ".join(f'<path d="M {x} 0 v 25" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def generate_skills_svg():
    """Generates the upgraded Super Mario Bros 3 Reserve Inventory Tray."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 320" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}
      .cloud {{ fill: #ffffff; }}

      .text-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 13px;
        fill: #ffffff;
        stroke: #000000;
        stroke-width: 2.5;
        paint-order: stroke fill;
      }}

      .text-cat {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8.5px;
        fill: #b83c18;
        font-weight: bold;
      }}

      .text-item {{
        font-family: 'Press Start 2P', monospace;
        font-size: 7.5px;
        fill: #000000;
      }}

      .item-slot {{
        fill: #fde6c7;
        stroke: #000000;
        stroke-width: 2;
        transition: all 0.3s ease;
      }}

      .dialogue-panel-bg {{
        fill: #fce4a0;
        stroke: #000000;
        stroke-width: 3.5;
      }}
      .dialogue-panel-inner {{
        fill: none;
        stroke: #b83c18;
        stroke-width: 1.5;
      }}

      .item-active-1 {{ animation: activeItem 4s infinite ease-in-out; }}
      .item-active-2 {{ animation: activeItem 4s infinite ease-in-out 1s; }}
      .item-active-3 {{ animation: activeItem 4s infinite ease-in-out 2s; }}
      .item-active-4 {{ animation: activeItem 4s infinite ease-in-out 3s; }}

      @keyframes activeItem {{
        0%, 100% {{ fill: #fde6c7; stroke: #000000; }}
        50% {{ fill: #ffffff; stroke: #b83c18; }}
      }}

      .cloud-bg-1 {{ animation: cloudDrift 60s infinite linear; }}
      .cloud-bg-2 {{ animation: cloudDrift 90s infinite linear -45s; }}

      @keyframes cloudDrift {{
        0% {{ transform: translateX(850px); }}
        100% {{ transform: translateX(-200px); }}
      }}
    </style>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="320" class="bg-sky"/>

  <!-- Clouds -->
  <g class="cloud-bg-1" transform="translate(150, 10)">
    <path d="M120,20 C110,20 100,28 100,38 C90,38 80,46 80,56 C80,66 90,74 100,74 L160,74 C170,74 180,66 180,56 C180,46 170,38 160,38 C160,28 150,20 140,20 Z" class="cloud" opacity="0.6"/>
  </g>
  <g class="cloud-bg-2" transform="translate(550, 20)">
    <path d="M60,10 C55,10 50,14 50,19 C45,19 40,23 40,28 C40,33 45,37 50,37 L80,37 C85,37 90,33 90,28 C90,23 85,19 80,19 C80,14 75,10 70,10 Z" class="cloud" opacity="0.5"/>
  </g>

  <!-- Screen Header -->
  <text x="425" y="32" class="text-title" text-anchor="middle">> HERO EQUIPMENT &amp; SKILLS INVENTORY &lt;</text>

  <!-- Main inventory board -->
  <rect x="25" y="45" width="800" height="235" rx="10" class="dialogue-panel-bg"/>
  <rect x="31" y="51" width="788" height="223" rx="6" class="dialogue-panel-inner"/>

  <!-- CATEGORY 1: LANGUAGES -->
  <text x="45" y="75" class="text-cat">/WEAPONS_LANGUAGES</text>
  <rect x="45" y="87" width="175" height="36" rx="4" class="item-slot item-active-1"/>
  <text x="55" y="109" class="text-item">🐍 Python [LV99]</text>
  <rect x="45" y="131" width="175" height="36" rx="4" class="item-slot"/>
  <text x="55" y="153" class="text-item">🔷 TypeScript [LV95]</text>
  <rect x="45" y="175" width="175" height="36" rx="4" class="item-slot"/>
  <text x="55" y="197" class="text-item">💛 JavaScript [LV95]</text>
  <rect x="45" y="219" width="175" height="36" rx="4" class="item-slot"/>
  <text x="55" y="241" class="text-item">🦀 Rust [LV92]</text>

  <!-- CATEGORY 2: FRAMEWORKS -->
  <text x="240" y="75" class="text-cat">/ARMOR_FRAMEWORKS</text>
  <rect x="240" y="87" width="175" height="36" rx="4" class="item-slot"/>
  <text x="250" y="109" class="text-item">▲ Next.js [LV90]</text>
  <rect x="240" y="131" width="175" height="36" rx="4" class="item-slot item-active-2"/>
  <text x="250" y="153" class="text-item">⚛️ React [LV90]</text>
  <rect x="240" y="175" width="175" height="36" rx="4" class="item-slot"/>
  <text x="250" y="197" class="text-item">🟢 Node.js [LV90]</text>
  <rect x="240" y="219" width="175" height="36" rx="4" class="item-slot"/>
  <text x="250" y="241" class="text-item">🍞 Bun [LV85]</text>

  <!-- CATEGORY 3: DATABASES -->
  <text x="435" y="75" class="text-cat">/POTIONS_DATABASES</text>
  <rect x="435" y="87" width="175" height="36" rx="4" class="item-slot"/>
  <text x="445" y="109" class="text-item">🐘 PostgreSQL [LV88]</text>
  <rect x="435" y="131" width="175" height="36" rx="4" class="item-slot"/>
  <text x="445" y="153" class="text-item">⏏️ Prisma [LV85]</text>
  <rect x="435" y="175" width="175" height="36" rx="4" class="item-slot item-active-3"/>
  <text x="445" y="197" class="text-item">📊 SQL Query [LV88]</text>
  <rect x="435" y="219" width="175" height="36" rx="4" class="item-slot"/>
  <text x="445" y="241" class="text-item">🎨 Tailwind [LV95]</text>

  <!-- CATEGORY 4: AI & DEVOPS -->
  <text x="630" y="75" class="text-cat">/SPELLS_AI_DEVOPS</text>
  <rect x="630" y="87" width="175" height="36" rx="4" class="item-slot"/>
  <text x="640" y="109" class="text-item">🤖 Python AI [LV92]</text>
  <rect x="630" y="131" width="175" height="36" rx="4" class="item-slot"/>
  <text x="640" y="153" class="text-item">🧠 RAG / LLM [LV92]</text>
  <rect x="630" y="175" width="175" height="36" rx="4" class="item-slot"/>
  <text x="640" y="197" class="text-item">🐳 Docker [LV82]</text>
  <rect x="630" y="219" width="175" height="36" rx="4" class="item-slot item-active-4"/>
  <text x="640" y="241" class="text-item">🐙 Git / CI-CD [LV92]</text>

  <!-- Ground -->
  <g transform="translate(0, 295)">
    <rect width="850" height="6" fill="#fc9838"/>
    <rect y="6" width="850" height="19" fill="#b83c18"/>
    <path d="M 0 6 L 850 6 M 0 14 L 850 14" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>
    {" ".join(f'<path d="M {x} 0 v 25" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def generate_performance_metrics_svg(stats):
    """Generates the Super Mario Arcade Performance Metrics Board replacing generic third-party cards."""
    langs = [
        ('HTML/Web', 54.7, '#e34c26', '🌐'),
        ('TypeScript', 30.7, '#3178c6', '🔷'),
        ('Python', 7.1, '#3572A5', '🐍'),
        ('JavaScript', 5.0, '#f1e05a', '💛'),
        ('Rust', 1.2, '#dea584', '🦀'),
        ('Shell/Other', 1.3, '#89e051', '🐚')
    ]

    bar_rects = []
    curr_x = 0
    total_bar_w = 330
    for name, pct, col, icon in langs:
        seg_w = max(4, int((pct / 100.0) * total_bar_w))
        bar_rects.append(f'<rect x="{curr_x}" y="0" width="{seg_w}" height="12" fill="{col}"/>')
        curr_x += seg_w

    lang_rows = []
    col1 = langs[:3]
    col2 = langs[3:]
    for i in range(3):
        y = 52 + i * 28
        name1, pct1, col1_c, icon1 = col1[i]
        lang_rows.append(f'''
    <g transform="translate(20, {y})">
      <circle cx="6" cy="6" r="4" fill="{col1_c}" stroke="#000" stroke-width="1"/>
      <text x="16" y="9" font-family="'Press Start 2P', monospace" font-size="7.5" fill="#000000">{name1} {pct1}%</text>
    </g>''')
        name2, pct2, col2_c, icon2 = col2[i]
        lang_rows.append(f'''
    <g transform="translate(195, {y})">
      <circle cx="6" cy="6" r="4" fill="{col2_c}" stroke="#000" stroke-width="1"/>
      <text x="16" y="9" font-family="'Press Start 2P', monospace" font-size="7.5" fill="#000000">{name2} {pct2}%</text>
    </g>''')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 440" width="100%" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      {PRESS_START_FONT}

      .bg-sky {{ fill: #5c94fc; }}
      .cloud {{ fill: #ffffff; }}

      .text-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 13px;
        fill: #ffffff;
        stroke: #000000;
        stroke-width: 2.5;
        paint-order: stroke fill;
      }}
      .panel-title {{
        font-family: 'Press Start 2P', monospace;
        font-size: 9.5px;
        fill: #b83c18;
        font-weight: bold;
      }}
      .stat-label {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #4a3728;
        font-weight: bold;
      }}
      .stat-val {{
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        fill: #008800;
        font-weight: bold;
      }}
      .box-container {{
        fill: #fce4a0;
        stroke: #000000;
        stroke-width: 3.5;
      }}
      .box-inner {{
        fill: none;
        stroke: #b83c18;
        stroke-width: 1.5;
      }}

      /* Streak Ring Pulse */
      .streak-ring {{
        animation: flameRingPulse 2s infinite ease-in-out;
      }}
      @keyframes flameRingPulse {{
        0%, 100% {{ stroke: #e52521; stroke-width: 3.5; }}
        50% {{ stroke: #fc9838; stroke-width: 5; }}
      }}

      .star-spin {{
        animation: starSpinBob 2s infinite ease-in-out;
      }}
      @keyframes starSpinBob {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-3px); }}
      }}

      .cloud-bg-1 {{ animation: cloudDrift 60s infinite linear; }}
      .cloud-bg-2 {{ animation: cloudDrift 90s infinite linear -30s; }}

      @keyframes cloudDrift {{
        0% {{ transform: translateX(850px); }}
        100% {{ transform: translateX(-200px); }}
      }}
    </style>
  </defs>

  <!-- Sky Background -->
  <rect width="850" height="440" class="bg-sky"/>

  <!-- Clouds -->
  <g class="cloud-bg-1" transform="translate(80, 10)">
    <path d="M120,20 C110,20 100,28 100,38 C90,38 80,46 80,56 C80,66 90,74 100,74 L160,74 C170,74 180,66 180,56 C180,46 170,38 160,38 C160,28 150,20 140,20 Z" class="cloud" opacity="0.6"/>
  </g>
  <g class="cloud-bg-2" transform="translate(520, 20)">
    <path d="M60,10 C55,10 50,14 50,19 C45,19 40,23 40,28 C40,33 45,37 50,37 L80,37 C85,37 90,33 90,28 C90,23 85,19 80,19 C80,14 75,10 70,10 Z" class="cloud" opacity="0.5"/>
  </g>

  <!-- Title -->
  <text x="425" y="32" class="text-title" text-anchor="middle">> SYSTEM PERFORMANCE METRICS &lt;</text>

  <!-- CARD 1: GITHUB ARCADE STATS (Top Left) -->
  <g transform="translate(35, 48)">
    <rect width="375" height="195" rx="8" class="box-container"/>
    <rect x="6" y="6" width="363" height="183" rx="5" class="box-inner"/>
    <rect x="8" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="357" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="8" y="177" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="357" y="177" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>

    <text x="24" y="28" class="panel-title">> SUJITH GITHUB STATS</text>

    <!-- Star Count -->
    <g transform="translate(24, 48)">
      <polygon points="6,0 8,4 12,4 9,7 10,12 6,9 2,12 3,7 0,4 4,4" fill="#fcf800" stroke="#000" stroke-width="1"/>
      <text x="20" y="9" class="stat-label">TOTAL STARS EARNED:</text>
      <text x="260" y="9" class="stat-val">{stats['stars']}</text>
    </g>

    <!-- Commits -->
    <g transform="translate(24, 76)">
      <circle cx="6" cy="6" r="5" fill="#a85400" stroke="#000" stroke-width="1"/>
      <text x="20" y="9" class="stat-label">TOTAL COMMITS:</text>
      <text x="260" y="9" class="stat-val">{stats['commits']}</text>
    </g>

    <!-- PRs -->
    <g transform="translate(24, 104)">
      <circle cx="6" cy="6" r="5" fill="#00a800" stroke="#000" stroke-width="1"/>
      <text x="20" y="9" class="stat-label">TOTAL PRS MERGED:</text>
      <text x="260" y="9" class="stat-val">{stats['prs']}</text>
    </g>

    <!-- Issues -->
    <g transform="translate(24, 132)">
      <circle cx="6" cy="6" r="5" fill="#fc9838" stroke="#000" stroke-width="1"/>
      <text x="20" y="9" class="stat-label">TOTAL ISSUES CLOSED:</text>
      <text x="260" y="9" class="stat-val">{stats['issues']}</text>
    </g>

    <!-- Rank Tier -->
    <g transform="translate(24, 160)">
      <text x="20" y="9" class="stat-label">CONTRIBUTION TIER:</text>
      <text x="220" y="9" font-family="'Press Start 2P', monospace" font-size="8" fill="#e52521" font-weight="bold">S-TIER ★★★</text>
    </g>
  </g>

  <!-- CARD 2: MOST USED POWER-UP LANGUAGES (Top Right) -->
  <g transform="translate(440, 48)">
    <rect width="375" height="195" rx="8" class="box-container"/>
    <rect x="6" y="6" width="363" height="183" rx="5" class="box-inner"/>
    <rect x="8" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="357" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="8" y="177" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="357" y="177" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>

    <text x="24" y="28" class="panel-title">> MOST USED LANGUAGES</text>

    <!-- Multi-Color Segmented Power-Up Bar -->
    <g transform="translate(22, 38)">
      <rect width="332" height="14" rx="3" fill="#111111" stroke="#000" stroke-width="1.5"/>
      <g transform="translate(1, 1)" clip-path="url(#bar-clip)">
        {"".join(bar_rects)}
      </g>
      <clipPath id="bar-clip">
        <rect width="330" height="12" rx="2"/>
      </clipPath>
    </g>

    <!-- 2 Column Language List -->
    <g transform="translate(4, 12)">
      {"".join(lang_rows)}
    </g>
  </g>

  <!-- CARD 3: CONTINUOUS ADVENTURE & STREAK (Bottom Full Width) -->
  <g transform="translate(35, 258)">
    <rect width="780" height="145" rx="8" class="box-container"/>
    <rect x="6" y="6" width="768" height="133" rx="5" class="box-inner"/>
    <rect x="8" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="762" y="8" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="8" y="127" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>
    <rect x="762" y="127" width="10" height="10" fill="#fc9838" stroke="#000" stroke-width="1"/>

    <!-- Column 1: Total Contributions -->
    <g transform="translate(130, 40)">
      <text x="0" y="24" font-family="'Press Start 2P', monospace" font-size="20" fill="#000000" font-weight="bold" text-anchor="middle">1,600</text>
      <text x="0" y="52" font-family="'Press Start 2P', monospace" font-size="8" fill="#4a3728" font-weight="bold" text-anchor="middle">TOTAL CONTRIBUTIONS</text>
      <text x="0" y="74" font-family="'Press Start 2P', monospace" font-size="7" fill="#b83c18" text-anchor="middle">Oct 4, 2024 - Present</text>
    </g>

    <!-- Divider Line 1 -->
    <line x1="260" y1="25" x2="260" y2="120" stroke="#b83c18" stroke-width="1.5" stroke-dasharray="3 3"/>

    <!-- Column 2: Current Streak (Center Hero) -->
    <g transform="translate(390, 20)">
      <!-- Flame Icon on Top -->
      <g transform="translate(-8, 5)" class="star-spin">
        <path d="M 8 0 C 4 6, 2 10, 8 16 C 14 10, 12 6, 8 0 Z" fill="#e52521"/>
        <path d="M 8 4 C 6 8, 4 10, 8 13 C 12 10, 10 8, 8 4 Z" fill="#fc9838"/>
      </g>
      <!-- Circular Combo Ring -->
      <circle cx="0" cy="46" r="28" fill="#ffffff" stroke="#e52521" stroke-width="4" class="streak-ring"/>
      <text x="0" y="54" font-family="'Press Start 2P', monospace" font-size="22" fill="#000000" font-weight="bold" text-anchor="middle">1</text>

      <text x="0" y="92" font-family="'Press Start 2P', monospace" font-size="8.5" fill="#b83c18" font-weight="bold" text-anchor="middle">CURRENT COMBO</text>
      <text x="0" y="108" font-family="'Press Start 2P', monospace" font-size="7" fill="#008800" font-weight="bold" text-anchor="middle">★ STAGE ACTIVE TODAY ★</text>
    </g>

    <!-- Divider Line 2 -->
    <line x1="520" y1="25" x2="520" y2="120" stroke="#b83c18" stroke-width="1.5" stroke-dasharray="3 3"/>

    <!-- Column 3: Longest Streak -->
    <g transform="translate(650, 40)">
      <text x="0" y="24" font-family="'Press Start 2P', monospace" font-size="20" fill="#000000" font-weight="bold" text-anchor="middle">8</text>
      <text x="0" y="52" font-family="'Press Start 2P', monospace" font-size="8" fill="#4a3728" font-weight="bold" text-anchor="middle">LONGEST STREAK</text>
      <text x="0" y="74" font-family="'Press Start 2P', monospace" font-size="7" fill="#b83c18" text-anchor="middle">Apr 14 - Apr 21 Record</text>
    </g>
  </g>

  <!-- Ground Terrain -->
  <g transform="translate(0, 415)">
    <rect width="850" height="5" fill="#fc9838"/>
    <rect y="5" width="850" height="20" fill="#b83c18"/>
    <path d="M 0 5 L 850 5 M 0 12 L 850 12" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>
    {" ".join(f'<path d="M {x} 0 v 25" stroke="#000" stroke-width="1" stroke-opacity="0.3"/>' for x in range(20, 850, 20))}
  </g>
</svg>"""
    return svg

def update_all_svgs():
    """Main routine to fetch real data and update all SVGs."""
    username = "sujithputta02"
    print(f"--- Fetching real-time stats for {username} ---")
    stats = fetch_github_data(username)
    print(f"Stats fetched: {stats['public_repos']} repos, {stats['stars']} stars, {stats['commits']} commits, {stats['followers']} followers")
    print(f"Featured repos: {[r['name'] for r in stats['featured_repos']]}")

    os.makedirs("public", exist_ok=True)
    os.makedirs("public/quests", exist_ok=True)

    # 1. Update header.svg
    header_svg = generate_header_svg(stats)
    with open("public/header.svg", "w", encoding="utf-8") as f:
        f.write(header_svg)
    print("✓ Updated public/header.svg")

    # 2. Update retro_stats.svg
    stats_svg = generate_retro_stats_svg(stats)
    with open("public/retro_stats.svg", "w", encoding="utf-8") as f:
        f.write(stats_svg)
    print("✓ Updated public/retro_stats.svg")

    # 3. Update adventure_quests.svg
    quests_svg = generate_adventure_quests_svg(stats)
    with open("public/adventure_quests.svg", "w", encoding="utf-8") as f:
        f.write(quests_svg)
    print("✓ Updated public/adventure_quests.svg")

    # 4. Generate individual quest cards
    for idx, repo in enumerate(stats['featured_repos'][:4], start=1):
        card_svg = generate_individual_quest_card(repo, idx)
        filename = f"public/quests/quest_{idx}.svg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(card_svg)
        print(f"✓ Generated {filename} for {repo.get('name')}")

    # 5. Update system_overview.svg
    overview_svg = generate_system_overview_svg(stats)
    with open("public/system_overview.svg", "w", encoding="utf-8") as f:
        f.write(overview_svg)
    print("✓ Updated public/system_overview.svg")

    # 6. Update skills.svg
    skills_svg = generate_skills_svg()
    with open("public/skills.svg", "w", encoding="utf-8") as f:
        f.write(skills_svg)
    print("✓ Updated public/skills.svg")

    # 7. Update performance_metrics.svg
    perf_svg = generate_performance_metrics_svg(stats)
    with open("public/performance_metrics.svg", "w", encoding="utf-8") as f:
        f.write(perf_svg)
    print("✓ Updated public/performance_metrics.svg")

    # Validate XML of all generated files
    for root, _, files in os.walk("public"):
        for f in files:
            if f.endswith(".svg"):
                fpath = os.path.join(root, f)
                try:
                    ET.parse(fpath)
                except Exception as xml_err:
                    print(f"XML Validation ERROR in {fpath}: {xml_err}")
                    raise xml_err
    print("✓ All SVGs passed XML validation successfully!")

if __name__ == "__main__":
    update_all_svgs()
