from flask import request, jsonify
import numpy as np
from . import api_bp

@api_bp.route('/api/polarized_light')
def get_polarized_light():
    """计算偏振光的电场分量。
    
    模拟偏振光传播，可用于演示线偏振、圆偏振和椭圆偏振。
    通过调节偏振片角度和相位差可以观察不同的偏振状态。

    请求参数:
        angle (float): 偏振片的旋转角度，单位度，默认值为0
        phase_diff (float): 两个正交分量间的相位差，单位弧度，默认值为0

    返回值:
        JSON对象，包含以下字段：
        - x (list[float]): 电场X分量数组
        - y (list[float]): 电场Y分量数组
        
    示例:
        GET /api/polarized_light?angle=45&phase_diff=1.57
    """
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