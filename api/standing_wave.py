from flask import request, jsonify
import numpy as np
from . import api_bp

@api_bp.route('/api/standing_wave')
def get_standing_wave_data():
    """生成驻波数据，包括前行波、反射波和合成波。
    
    驻波是由传播方向相反的两列相同波形叠加而成。计算包括波节点和波腹点的位置。

    请求参数:
        t (float): 时间点，单位秒，默认值为0
        k (float): 波数，单位rad/m，默认值为2π
        omega (float): 角频率，单位rad/s，默认值为2π
        amplitude (float): 波的振幅，默认值为1.0

    返回值:
        JSON对象，包含以下字段：
        - x (list[float]): 位置坐标数组
        - y (list[float]): 驻波振幅数组
        - forward_wave (list[float]): 前行波振幅数组
        - backward_wave (list[float]): 反射波振幅数组
        - nodes (list[float]): 波节点位置数组
        - antinodes (list[float]): 波腹点位置数组
        
    示例:
        GET /api/standing_wave?t=0&k=6.28&omega=6.28&amplitude=1.0
    """
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