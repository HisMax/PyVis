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
def diffraction():
    """计算矩形孔的夫琅禾费衍射图样。
    
    使用夫琅禾费衍射公式计算矩形孔的衍射光强分布。
    I(θx,θy) = I₀·sinc²(πa·sinθx/λ)·sinc²(πb·sinθy/λ)
    """
    # 获取参数
    wavelength = float(request.args.get('wavelength', 550))  # nm
    rect_width = float(request.args.get('rect_width', 0.0028))  # m
    rect_height = float(request.args.get('rect_height', 0.0026))  # m
    screen_distance = float(request.args.get('screen_distance', 1.6))  # m
    
    # 转换波长为米
    lambda_m = wavelength * 1e-9  # 转换为米
    
    # 计算第一个暗纹位置（用于确定合适的显示范围）
    x_dark = lambda_m * screen_distance / rect_width
    y_dark = lambda_m * screen_distance / rect_height
    
    # 使用暗纹位置的倍数作为显示范围（单位：mm）
    range_mm = max(x_dark, y_dark) * 10000  # 转换为mm并扩大范围
    
    # 计算网格
    N = 500  # 增加网格点数以提高分辨率
    x = np.linspace(-range_mm, range_mm, N)  # mm
    y = np.linspace(-range_mm, range_mm, N)  # mm
    X, Y = np.meshgrid(x, y)
    
    # 转换为弧度进行计算
    theta_x = np.arctan2(X * 1e-3, screen_distance)  # 转换为弧度
    theta_y = np.arctan2(Y * 1e-3, screen_distance)  # 转换为弧度
    
    # 计算衍射因子
    beta_x = np.pi * rect_width * np.sin(theta_x) / lambda_m
    beta_y = np.pi * rect_height * np.sin(theta_y) / lambda_m
    
    # 计算光强分布
    intensity = np.sinc(beta_x/np.pi)**2 * np.sinc(beta_y/np.pi)**2
    
    # 归一化
    intensity = intensity / np.max(intensity)
    
    # 对数缩放以突出细节，使用更合适的缩放因子
    scale_factor = 5  # 调整缩放因子以获得更好的对比度
    intensity = np.log1p(intensity * scale_factor) / np.log1p(scale_factor)
    
    # 计算第一级暗纹位置（用于显示）
    first_min_x = x_dark * 1000  # 转换为mm
    first_min_y = y_dark * 1000  # 转换为mm
    
    return jsonify({
        'x': x.tolist(),
        'y': y.tolist(),
        'intensity': intensity.tolist(),
        'x_range': float(range_mm),
        'y_range': float(range_mm),
        'first_min_x': float(first_min_x),
        'first_min_y': float(first_min_y)
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
    app.run(debug=True,port=5001)