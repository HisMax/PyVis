from flask import request, jsonify
import numpy as np
from . import api_bp

@api_bp.route('/api/diffraction')
def get_diffraction_pattern():
    """计算单缝衍射的光强分布。
    
    使用夫琅禾费衍射公式计算单缝衍射的光强分布。考虑了波长、狭缝宽度和屏距的影响。

    请求参数:
        wavelength (float): 光的波长，单位nm，默认值为500
        slit_width (float): 狭缝宽度，单位μm，默认值为100
        screen_distance (float): 接收屏到狭缝的距离，单位m，默认值为1

    返回值:
        JSON对象，包含以下字段：
        - x (list[float]): 接收屏上的位置坐标，单位mm
        - y (list[float]): 对应位置的相对光强
        
    示例:
        GET /api/diffraction?wavelength=500&slit_width=100&screen_distance=1
    """
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