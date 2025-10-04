from flask import Flask, send_file, request
from flask import Flask, send_file, request
from io import BytesIO
from random import choice, randint
import random  # For seeding

app = Flask(__name__)

# Core colors: Monad's purple-blue electric vibe
COLORS = {
    'core': ['#0A2540', '#1E3A8A', '#3730A3', '#7C3AED'],  # Added purple for meme energy
    'accent': ['#06B6D4', '#3B82F6', '#8B5CF6', '#EC4899'],  # Pops of pink for frog flair
    'bg': ['#000000', '#0F172A', '#1E293B', '#581C87']  # Dark purple bg nod to lore
}

# Top Monad memes to incorporate (pulled from community hits)
MEME_ELEMENTS = {
    'purple_frog': {'desc': 'Viral Pepe-frog mascot', 'color': '#7C3AED', 'shape': 'ellipse'},  # Frog eyes/hat
    'salmonad': {'desc': 'Cosmic fish lore', 'color': '#F59E0B', 'shape': 'polygon'},  # Fish scales/trail
    'mouch': {'desc': 'Underrated monanimal', 'color': '#10B981', 'shape': 'line'},  # Hedgehog spikes or sparks
    'mainnet_arc': {'desc': '2025 hype/wait', 'color': '#F97316', 'shape': 'text'},  # "Loading..." overlay
    'gmonad': {'desc': '#1 meme token', 'color': '#EF4444', 'shape': 'circle'}  # Coin emblem
}

def generate_monad_pfp(seed=None):
    if seed:
        random.seed(seed)
    
    from PIL import Image, ImageDraw, ImageFont
    
    # 512x512 canvas
    img = Image.new('RGB', (512, 512), choice(COLORS['bg']))
    draw = ImageDraw.Draw(img)
    
    # Base: Monad core (geometric power unit)
    core_shape = choice(['circle', 'triangle'])
    core_color = choice(COLORS['core'])
    center = (256, 256)
    if core_shape == 'circle':
        bbox = (128, 128, 384, 384)
        draw.ellipse(bbox, fill=core_color)
        inner_bbox = (160, 160, 352, 352)
        draw.ellipse(inner_bbox, fill=choice(COLORS['accent']))
    else:
        points = [(256, 100), (100, 412), (412, 412)]
        draw.polygon(points, fill=core_color)
        draw.line([(256, 100), (100, 412)], fill=choice(COLORS['accent']), width=8)
        draw.line([(256, 100), (412, 412)], fill=choice(COLORS['accent']), width=8)
    
    # Thrill elements: 2-4 dynamic accents
    num_elements = randint(2, 4)
    for _ in range(num_elements):
        elem_type = choice(['speed_line', 'node_glow', 'parallel_bar'])
        if elem_type == 'speed_line':
            x1, y1 = randint(0, 512), randint(0, 512)
            x2, y2 = randint(0, 512), randint(0, 512)
            draw.line([(x1, y1), (x2, y2)], fill=choice(COLORS['accent']), width=randint(2, 6))
        elif elem_type == 'node_glow':
            cx, cy = randint(50, 462), randint(50, 462)
            draw.ellipse((cx-10, cy-10, cx+10, cy+10), fill=choice(COLORS['accent']))
            draw.line([(cx, cy), center], fill=core_color, width=2)
        else:
            bar_y = randint(50, 462)
            draw.rectangle((50, bar_y-5, 462, bar_y+5), fill=choice(COLORS['accent']))
    
    # Meme infusion: Add 1-2 top meme elements for community thrill
    num_memes = randint(1, 2)
    for _ in range(num_memes):
        meme = choice(list(MEME_ELEMENTS.keys()))
        data = MEME_ELEMENTS[meme]
        mx, my = randint(50, 462), randint(50, 462)
        if data['shape'] == 'ellipse':  # Frog eyes or coin
            draw.ellipse((mx-15, my-15, mx+15, my+15), fill=data['color'])
            # Add "hat" or glow
            draw.ellipse((mx-20, my-25, mx+20, my-5), fill=data['color'], outline='white', width=2)
        elif data['shape'] == 'polygon':  # Salmonad fish
            fish_points = [(mx, my), (mx+30, my-10), (mx+40, my+10), (mx+30, my+30)]
            draw.polygon(fish_points, fill=data['color'])
            # Trail
            draw.line([(mx+40, my+10), (mx+60, my+10)], fill=data['color'], width=3)
        elif data['shape'] == 'line':  # Mouch spikes
            for i in range(3):
                angle = randint(0, 360)
                end_x = mx + randint(10, 20) * (1 if angle < 180 else -1)
                end_y = my + randint(10, 20) * (1 if angle % 90 < 45 else -1)
                draw.line([(mx, my), (end_x, end_y)], fill=data['color'], width=4)
        elif data['shape'] == 'text':  # Mainnet arc text
            try:
                font = ImageFont.truetype("arial.ttf", 24)  # Fallback to default if no font
            except:
                font = ImageFont.load_default()
            text = choice(["2025 Loading...", "Mainnet Arc 💜", "10k TPS When?"])
            draw.text((mx, my), text, fill=data['color'], font=font)
        else:  # Gmonad circle emblem
            draw.ellipse((mx-20, my-20, mx+20, my+20), fill=data['color'])
    
    # Return in-memory PNG
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

@app.route('/generate', methods=['GET'])
def generate_pfp():
    seed = request.args.get('seed', type=int)
    img_bytes = generate_monad_pfp(seed)
    return send_file(img_bytes, mimetype='image/png', as_attachment=False, download_name='nadforge_pfp.png')

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>NadForge: Monad Meme PFP Generator 💜</h1>
    <p>Forged for the Nad community—parallel power meets purple frogs. Hit <a href="/generate">/generate</a> for a random mint, or <a href="/generate?seed=42">/generate?seed=42</a> for Nad-proof vibes.</p>
    <img src="/generate?seed=123" alt="Sample NadForge PFP" style="max-width: 256px; border: 2px solid #7C3AED; border-radius: 8px;">
    <p><small>Powered by Monad's 10k TPS thrill. Share your forge: @monad</small></p>
    '''

if __name__ == '__main__':
    app.run(debug=True)