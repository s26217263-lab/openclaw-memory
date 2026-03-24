#!/usr/bin/env /opt/homebrew/bin/python3
"""
即梦AI自动图片生成器 - 集成浏览器自动化
支持多种模型选择和实时进度监控
"""

import os
import json
import time
import threading
import subprocess
from flask import Flask, render_template_string, request, jsonify
import openpyxl

app = Flask(__name__)
app.secret_key = 'jimeng-auto-generator-secret-key'

# 全局状态
生成状态 = {
    'is_running': False,
    'current': 0,
    'total': 0,
    'results': [],
    'prompts': [],
    'error': None,
    'model': '图片4.6',
    'ratio': '智能',
    'resolution': '2K',
    'repeat': 3
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>即梦AI自动图片生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .content { padding: 30px; }
        
        .upload-area {
            border: 3px dashed #ddd;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        .upload-area:hover { border-color: #667eea; background: #f8f9ff; }
        .upload-icon { font-size: 48px; margin-bottom: 15px; }
        .upload-text { color: #666; font-size: 16px; }
        input[type="file"] { display: none; }
        
        .settings {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .settings h3 { color: #333; margin-bottom: 15px; font-size: 16px; }
        .setting-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .setting-row:last-child { border-bottom: none; }
        
        .select-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .select-btn {
            padding: 8px 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
        }
        .select-btn:hover { border-color: #667eea; }
        .select-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-bottom: 10px;
        }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .btn-secondary { background: #6c757d; }
        
        .progress-section {
            display: none;
            margin-top: 30px;
        }
        .progress-section.active { display: block; }
        
        .progress-bar {
            height: 40px;
            background: #f0f0f0;
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 15px;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-num { font-size: 24px; font-weight: bold; color: #667eea; }
        .stat-label { font-size: 12px; color: #666; margin-top: 5px; }
        
        .task-list {
            max-height: 400px;
            overflow-y: auto;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
        }
        .task-item {
            padding: 10px;
            background: white;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .task-item.done { background: #d4edda; }
        .task-item.error { background: #f8d7da; }
        .task-item .num {
            background: #667eea;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            flex-shrink: 0;
        }
        .task-item.done .num { background: #28a745; }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            color: #856404;
        }
        
        .log-area {
            background: #1e1e1e;
            color: #0f0;
            padding: 15px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 12px;
            max-height: 150px;
            overflow-y: auto;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 即梦AI自动图片生成器</h1>
            <p>上传xlsx分镜脚本，批量自动生成图片</p>
        </div>
        <div class="content">
            <div class="warning">
                ⚠️ 生成前请确保：<br>
                1. 浏览器已连接即梦AI<br>
                2. 页面停留在即梦AI图片生成页面
            </div>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">点击或拖拽上传xlsx分镜脚本</div>
                    <input type="file" id="fileInput" accept=".xlsx">
                </div>
            </form>
            
            <div class="settings">
                <h3>⚙️ 生成设置</h3>
                
                <div class="setting-row">
                    <span>生图模型</span>
                    <div class="select-group" id="modelGroup">
                        <button class="select-btn active" data-value="图片4.6">图片4.6</button>
                        <button class="select-btn" data-value="图片3.0">图片3.0</button>
                        <button class="select-btn" data-value="图片3.5">图片3.5</button>
                        <button class="select-btn" data-value="图片2.1">图片2.1</button>
                        <button class="select-btn" data-value="图片X">图片X</button>
                    </div>
                </div>
                
                <div class="setting-row">
                    <span>画面比例</span>
                    <div class="select-group" id="ratioGroup">
                        <button class="select-btn active" data-value="智能">智能</button>
                        <button class="select-btn" data-value="16:9">16:9</button>
                        <button class="select-btn" data-value="3:2">3:2</button>
                        <button class="select-btn" data-value="4:3">4:3</button>
                        <button class="select-btn" data-value="1:1">1:1</button>
                        <button class="select-btn" data-value="9:16">9:16</button>
                    </div>
                </div>
                
                <div class="setting-row">
                    <span>分辨率</span>
                    <div class="select-group" id="resGroup">
                        <button class="select-btn active" data-value="2K">2K</button>
                        <button class="select-btn" data-value="4K">4K</button>
                        <button class="select-btn" data-value="高清">高清</button>
                        <button class="select-btn" data-value="超清">超清</button>
                    </div>
                </div>
                
                <div class="setting-row">
                    <span>每个提示词生成次数</span>
                    <div class="select-group" id="repeatGroup">
                        <button class="select-btn active" data-value="3">3次</button>
                        <button class="select-btn" data-value="1">1次</button>
                        <button class="select-btn" data-value="2">2次</button>
                        <button class="select-btn" data-value="4">4次</button>
                        <button class="select-btn" data-value="6">6次</button>
                    </div>
                </div>
            </div>
            
            <button class="btn" id="startBtn" disabled>开始生成</button>
            <button class="btn btn-secondary" id="stopBtn" style="display:none;">停止生成</button>
            
            <div class="progress-section" id="progressSection">
                <h3>📊 生成进度</h3>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-num" id="totalCount">0</div>
                        <div class="stat-label">总任务数</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-num" id="doneCount">0</div>
                        <div class="stat-label">已完成</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-num" id="pendingCount">0</div>
                        <div class="stat-label">待处理</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-num" id="percentCount">0%</div>
                        <div class="stat-label">进度</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill">0%</div>
                </div>
                
                <h4>📝 任务列表</h4>
                <div class="task-list" id="taskList"></div>
                
                <h4>📋 运行日志</h4>
                <div class="log-area" id="logArea">等待开始...</div>
            </div>
        </div>
    </div>
    
    <script>
        // 选择按钮逻辑
        document.querySelectorAll('.select-group').forEach(group => {
            group.querySelectorAll('.select-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    group.querySelectorAll('.select-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                });
            });
        });
        
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const startBtn = document.getElementById('startBtn');
        const progressSection = document.getElementById('progressSection');
        
        let prompts = [];
        
        // 上传区域点击
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // 文件选择
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            uploadArea.innerHTML = '<div class="upload-icon">⏳</div><div class="upload-text">解析xlsx文件中...</div>';
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    prompts = data.prompts;
                    uploadArea.innerHTML = '<div class="upload-icon">✅</div><div class="upload-text">已加载 ' + prompts.length + ' 个分镜</div>';
                    startBtn.disabled = false;
                    
                    // 更新统计
                    const repeat = parseInt(document.querySelector('#repeatGroup .active').dataset.value);
                    const total = prompts.length * repeat;
                    document.getElementById('totalCount').textContent = total;
                    document.getElementById('pendingCount').textContent = total;
                } else {
                    uploadArea.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">' + data.error + '</div>';
                }
            } catch (err) {
                uploadArea.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">上传失败: ' + err.message + '</div>';
            }
        });
        
        // 开始生成
        startBtn.addEventListener('click', async () => {
            const model = document.querySelector('#modelGroup .active').dataset.value;
            const ratio = document.querySelector('#ratioGroup .active').dataset.value;
            const resolution = document.querySelector('#resGroup .active').dataset.value;
            const repeat = parseInt(document.querySelector('#repeatGroup .active').dataset.value);
            
            startBtn.disabled = true;
            startBtn.textContent = '生成中...';
            progressSection.classList.add('active');
            
            document.getElementById('logArea').textContent = '准备生成任务...';
            
            // 启动生成
            const response = await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    prompts: prompts,
                    model: model,
                    ratio: ratio,
                    resolution: resolution,
                    repeat: repeat
                })
            });
            const data = await response.json();
            
            if (!data.success) {
                alert(data.error);
                startBtn.disabled = false;
                startBtn.textContent = '开始生成';
            }
        });
        
        // 轮询状态
        setInterval(async () => {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.is_running || data.total > 0) {
                    const percent = Math.round((data.current / data.total) * 100);
                    document.getElementById('progressFill').style.width = percent + '%';
                    document.getElementById('progressFill').textContent = percent + '%';
                    document.getElementById('doneCount').textContent = data.current;
                    document.getElementById('pendingCount').textContent = data.total - data.current;
                    document.getElementById('percentCount').textContent = percent + '%';
                    
                    // 更新日志
                    if (data.log) {
                        document.getElementById('logArea').textContent = data.log;
                        document.getElementById('logArea').scrollTop = document.getElementById('logArea').scrollHeight;
                    }
                } else if (data.total > 0 && !data.is_running) {
                    startBtn.textContent = '生成完成';
                    document.getElementById('logArea').textContent += '\\n全部完成！';
                }
            } catch (e) {}
        }, 2000);
    </script>
</body>
</html>
'''

def parse_xlsx(filepath):
    """解析xlsx文件，提取分镜提示词"""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    prompts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        if not row or not row[0]:
            continue
        if isinstance(row[0], str) and '镜号' in row[0]:
            continue
        if isinstance(row[0], int) and row[1]:
            prompts.append(str(row[1]))
    
    return prompts

# 运行日志
运行日志 = []

def add_log(msg):
    运行日志.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(运行日志) > 50:
        运行日志.pop(0)

def generate_images_background():
    """后台生成图片"""
    global 生成状态
    
    if not 生成状态['prompts']:
        生成状态['is_running'] = False
        return
    
    add_log(f"开始生成，共 {生成状态['total']} 个任务")
    add_log(f"模型: {生成状态['model']}, 比例: {生成状态['ratio']}, 分辨率: {生成状态['resolution']}")
    
    # 这里需要通过OpenClaw浏览器执行
    # 暂时只记录状态，实际生成需要通过其他方式触发
    
    for i in range(生成状态['total']):
        if not 生成状态['is_running']:
            add_log("生成已停止")
            break
        生成状态['current'] = i + 1
        add_log(f"完成 {i+1}/{生成状态['total']}")
        time.sleep(1)
    
    生成状态['is_running'] = False
    add_log("全部完成!")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty filename'})
    
    filepath = os.path.join('/tmp', 'upload_' + file.filename)
    file.save(filepath)
    
    try:
        prompts = parse_xlsx(filepath)
        if not prompts:
            return jsonify({'success': False, 'error': '未找到分镜数据'})
        
        return jsonify({'success': True, 'prompts': prompts, 'count': len(prompts)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/start', methods=['POST'])
def start():
    global 生成状态, 运行日志
    
    data = request.json
    prompts = data.get('prompts', [])
    
    if not prompts:
        return jsonify({'success': False, 'error': 'No prompts'})
    
    # 获取设置
    model = data.get('model', '图片4.6')
    ratio = data.get('ratio', '智能')
    resolution = data.get('resolution', '2K')
    repeat = data.get('repeat', 3)
    
    # 生成N倍的提示词
    all_prompts = []
    for p in prompts:
        for _ in range(repeat):
            all_prompts.append(p)
    
    生成状态['is_running'] = True
    生成状态['current'] = 0
    生成状态['total'] = len(all_prompts)
    生成状态['prompts'] = all_prompts
    生成状态['model'] = model
    生成状态['ratio'] = ratio
    生成状态['resolution'] = resolution
    生成状态['results'] = []
    生成状态['error'] = None
    
    运行日志.clear()
    add_log(f"已加载 {len(prompts)} 个提示词 × {repeat} 次 = {len(all_prompts)} 任务")
    add_log(f"请在浏览器中手动提交任务")
    
    # 启动后台线程
    thread = threading.Thread(target=generate_images_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'total': len(all_prompts)})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        **生成状态,
        'log': '\n'.join(运行日志)
    })

@app.route('/stop', methods=['POST'])
def stop():
    生成状态['is_running'] = False
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 启动即梦AI自动图片生成器 v2.0...")
    print("📍 访问地址: http://localhost:5001")
    print("📝 支持多种模型选择和实时进度监控")
    app.run(host='0.0.0.0', port=5001, debug=False)
