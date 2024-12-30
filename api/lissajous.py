from flask import request, jsonify
import numpy as np
from . import api_bp

@api_bp.route('/api/lissajous')
def get_lissajous_data():
    """生成利萨如图形的数据点。
    
    利萨如图形是两个正交方向简谐振动合成的轨迹。通过调节两个方向的频率比和相位差，
    可以得到不同的图形。

    请求参数:
        freq_x (float): X方向振动的频率，默认值为3
        freq_y (float): Y方向振动的频率，默认值为2
        phase (float): 两个振动间的相位差，单位为弧度，默认值为π/2

    返回值:
        JSON对象，包含以下字段：
        - x (list[float]): X方向位移数组，长度1000
        - y (list[float]): Y方向位移数组，长度1000
        
    示例:
        GET /api/lissajous?freq_x=3&freq_y=2&phase=1.57
    """
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