from flask import Flask, render_template, jsonify, request
import numpy as np
from scipy.special import jv  # 用于衍射图样计算

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lissajous')
def get_lissajous_data():
    # 从请求参数获取频率和相位
    freq_x = float(request.args.get('freq_x', 3))
    freq_y = float(request.args.get('freq_y', 2))
    phase = float(request.args.get('phase', np.pi/2))
    
    # 生成利萨如图形数据
    t = np.linspace(0, 2*np.pi, 1000)
    A = 1  # 振幅
    
    x = A * np.sin(freq_x*t + phase)
    y = A * np.sin(freq_y*t)
    
    return jsonify({
        'x': x.tolist(),
        'y': y.tolist()
    })

@app.route('/api/standing_wave')
def get_standing_wave_data():
    # 从请求参数获取时间
    t = float(request.args.get('t', 0))
    k = float(request.args.get('k', 2*np.pi))
    omega = float(request.args.get('omega', 2*np.pi))
    amplitude = float(request.args.get('amplitude', 1.0))
    
    # 生成驻波数据
    x = np.linspace(0, 1, 200)  # 增加采样点以获得更平滑的曲线
    
    # 计算行波和驻波
    forward_wave = amplitude * np.cos(k*x - omega*t)  # 前行波
    backward_wave = amplitude * np.cos(k*x + omega*t)  # 反射波
    standing_wave = forward_wave + backward_wave  # 驻波
    
    # 计算波节点和波腹点位置
    wavelength = 2*np.pi/k
    nodes = np.array([i*wavelength/2 for i in range(int(1/wavelength*2)+1)])
    antinodes = np.array([(i+0.5)*wavelength/2 for i in range(int(1/wavelength*2))])
    
    return jsonify({
        'x': x.tolist(),
        'y': standing_wave.tolist(),
        'forward_wave': forward_wave.tolist(),
        'backward_wave': backward_wave.tolist(),
        'nodes': nodes.tolist(),
        'antinodes': antinodes.tolist()
    })

@app.route('/api/polarized_light')
def get_polarized_light():
    angle = float(request.args.get('angle', 0))
    phase_diff = float(request.args.get('phase_diff', 0))
    
    # 生成时间序列
    t = np.linspace(0, 2*np.pi, 200)
    
    # 计算原始电场分量
    Ex = np.cos(t)
    Ey = np.cos(t + phase_diff)
    
    # 应用旋转变换
    angle_rad = angle * np.pi / 180
    Ex_rot = Ex * np.cos(angle_rad) - Ey * np.sin(angle_rad)
    Ey_rot = Ex * np.sin(angle_rad) + Ey * np.cos(angle_rad)
    
    return jsonify({
        'x': Ex_rot.tolist(),
        'y': Ey_rot.tolist()
    })

@app.route('/api/diffraction')
def get_diffraction_pattern():
    wavelength = float(request.args.get('wavelength', 500))  # nm
    slit_width = float(request.args.get('slit_width', 100))  # μm
    screen_distance = float(request.args.get('screen_distance', 1))  # m
    
    # 计算衍射图样
    x = np.linspace(-5, 5, 1000)  # mm
    k = 2 * np.pi / (wavelength * 1e-9)
    alpha = k * slit_width * 1e-6 * x * 1e-3 / (2 * screen_distance)
    intensity = (np.sin(alpha) / alpha) ** 2
    
    return jsonify({
        'x': x.tolist(),
        'y': intensity.tolist()
    })

@app.route('/api/wave_superposition')
def get_wave_superposition():
    amp1 = float(request.args.get('amp1', 1))
    freq1 = float(request.args.get('freq1', 1))
    amp2 = float(request.args.get('amp2', 1))
    freq2 = float(request.args.get('freq2', 2))
    phase = float(request.args.get('phase', 0))
    
    x = np.linspace(0, 10, 500)
    wave1 = amp1 * np.sin(2*np.pi*freq1*x)
    wave2 = amp2 * np.sin(2*np.pi*freq2*x + phase)
    superposition = wave1 + wave2
    
    return jsonify({
        'x': x.tolist(),
        'wave1': wave1.tolist(),
        'wave2': wave2.tolist(),
        'superposition': superposition.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)