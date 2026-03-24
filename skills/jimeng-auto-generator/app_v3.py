#!/usr/bin/env python3
"""
即梦AI自动图片生成器 v3.0
支持队列管理、实时进度追踪
"""
import os
import json
import time
import threading
from flask import Flask, render_template_string, request, jsonify
import openpyxl

app = Flask(__name__)
app.secret_key = 'jimeng-v3-secret-key'

# 任务状态
class Task:
    def __init__(self, id, prompt, repeat=1):
        self.id = id
        self.prompt = prompt
        self.repeat = repeat
        self.status = 'pending'  # pending, submitting, generating, done, error
        self.submit_time = None
        self.complete_time = None
        self.error = None

# 全局状态
状态 = {
    'is_running': False,
    'tasks': [],  # Task objects
    'current_index': 0,
    'settings': {
        'model': '图片4.6',
        'ratio': '16:9',
        'resolution': '2K',
        'repeat': 3
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>即梦AI批量图片生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 25px 30px;
        }
        .header h1 { font-size: 24px; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 14px; }
        
        .content { padding: 25px; }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            color: #856404;
            font-size: 14px;
        }
        
        .row { display: flex; gap: 20px; margin-bottom: 20px; }
        .col { flex: 1; }
        
        .upload-area {
            border: 3px dashed #ddd;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover { border-color: #1e3c72; background: #f8f9ff; }
        .upload-icon { font-size: 36px; margin-bottom: 10px; }
        .upload-text { color: #666; }
        input[type="file"] { display: none; }
        
        .settings {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
        }
        .settings h3 { color: #333; margin-bottom: 15px; font-size: 16px; }
        
        .setting-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
        }
        
        .select-group { display: flex; gap: 8px; flex-wrap: wrap; }
        .select-btn {
            padding: 6px 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }
        .select-btn:hover { border-color: #1e3c72; }
        .select-btn.active { background: #1e3c72; color: white; border-color: #1e3c72; }
        
        .btn {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
            margin-right: 10px;
        }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .btn-danger { background: #dc3545; }
        
        .stats-bar {
            display: flex;
            gap: 15px;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .stat-item {
            flex: 1;
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }
        .stat-num { font-size: 24px; font-weight: bold; color: #1e3c72; }
        .stat-label { font-size: 12px; color: #666; margin-top: 4px; }
        
        .progress-full {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            width: 0%;
            transition: width 0.3s;
        }
        
        .queue-section { margin-top: 25px; }
        .queue-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            margin-bottom: 15px; 
        }
        
        .queue-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .queue-table th {
            background: #1e3c72;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 500;
        }
        .queue-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #eee;
        }
        .queue-table tr:hover { background: #f8f9ff; }
        
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .status-pending { background: #e9ecef; color: #666; }
        .status-submitting { background: #fff3cd; color: #856404; }
        .status-generating { background: #cce5ff; color: #004085; }
        .status-done { background: #d4edda; color: #155724; }
        .status-error { background: #f8d7da; color: #721c24; }
        
        .progress-cell { width: 100px; }
        .progress-mini {
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
        }
        .progress-mini-fill {
            height: 100%;
            background: #28a745;
            width: 0%;
        }
        
        .log-area {
            background: #1e1e1e;
            color: #0f0;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            max-height: 150px;
            overflow-y: auto;
            margin-top: 20px;
        }
        
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 即梦AI批量图片生成器</h1>
            <p>上传xlsx分镜脚本，批量自动生成图片 | 实时追踪进度</p>
        </div>
        <div class="content">
            <div class="warning">
                ⚠️ 生成前请确保：<br>
                1. 浏览器已连接即梦AI | 2. 页面停留在即梦AI图片生成页面 | 3. 比例已设为16:9
            </div>
            
            <div class="row">
                <div class="col">
                    <form id="uploadForm" enctype="multipart/form-data">
                        <div class="upload-area" id="uploadArea">
                            <div class="upload-icon">📁</div>
                            <div class="upload-text">点击上传xlsx分镜脚本</div>
                            <input type="file" id="fileInput" accept=".xlsx">
                        </div>
                    </form>
                </div>
                <div class="col">
                    <div class="settings">
                        <h3>⚙️ 生成设置</h3>
                        
                        <div class="setting-row">
                            <span>生图模型</span>
                            <div class="select-group" id="modelGroup">
                                <button class="select-btn active" data-value="图片4.6">图片4.6</button>
                                <button class="select-btn" data-value="图片5.0 Lite">图片5.0 Lite</button>
                                <button class="select-btn" data-value="图片3.0">图片3.0</button>
                            </div>
                        </div>
                        
                        <div class="setting-row">
                            <span>画面比例</span>
                            <div class="select-group" id="ratioGroup">
                                <button class="select-btn active" data-value="16:9">16:9</button>
                                <button class="select-btn" data-value="智能">智能</button>
                                <button class="select-btn" data-value="3:2">3:2</button>
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
                            </div>
                        </div>
                        
                        <div class="setting-row">
                            <span>每个提示词生成次数</span>
                            <div class="select-group" id="repeatGroup">
                                <button class="select-btn active" data-value="3">3次</button>
                                <button class="select-btn" data-value="1">1次</button>
                                <button class="select-btn" data-value="2">2次</button>
                                <button class="select-btn" data-value="4">4次</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="btn-group">
                <button class="btn" id="startBtn" disabled>开始生成</button>
                <button class="btn btn-danger" id="clearBtn">清空队列</button>
            </div>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-num" id="totalCount">0</div>
                    <div class="stat-label">总任务数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-num" id="doneCount">0</div>
                    <div class="stat-label">已完成</div>
                </div>
                <div class="stat-item">
                    <div class="stat-num" id="pendingCount">0</div>
                    <div class="stat-label">待处理</div>
                </div>
                <div class="stat-item">
                    <div class="stat-num" id="progressPercent">0%</div>
                    <div class="stat-label">总体进度</div>
                </div>
            </div>
            
            <div class="progress-full">
                <div class="progress-fill" id="progressBar"></div>
            </div>
            
            <div class="queue-section">
                <div class="queue-header">
                    <h3>📋 任务队列</h3>
                    <span id="queueInfo">共 0 个任务</span>
                </div>
                
                <table class="queue-table">
                    <thead>
                        <tr>
                            <th style="width:50px;">#</th>
                            <th style="width:40px;">状态</th>
                            <th>提示词内容</th>
                            <th style="width:80px;">提交时间</th>
                            <th style="width:80px;">完成时间</th>
                            <th style="width:100px;">进度</th>
                        </tr>
                    </thead>
                    <tbody id="queueBody">
                        <tr><td colspan="6" style="text-align:center;color:#999;">请先上传xlsx文件</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="log-area" id="logArea">等待操作...</div>
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
        
        let tasks = [];
        
        // 上传
        uploadArea.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            uploadArea.innerHTML = '<div class="upload-icon">⏳</div><div class="upload-text">解析中...</div>';
            
            try {
                const response = await fetch('/upload', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.success) {
                    tasks = data.tasks;
                    uploadArea.innerHTML = '<div class="upload-icon">✅</div><div class="upload-text">已加载 ' + tasks.length + ' 个任务</div>';
                    startBtn.disabled = false;
                    updateQueueTable();
                    addLog('已加载 ' + tasks.length + ' 个任务');
                } else {
                    uploadArea.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">' + data.error + '</div>';
                }
            } catch (err) {
                uploadArea.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">错误: ' + err.message + '</div>';
            }
        });
        
        // 清空队列
        document.getElementById('clearBtn').addEventListener('click', async () => {
            await fetch('/clear', { method: 'POST' });
            tasks = [];
            startBtn.disabled = true;
            uploadArea.innerHTML = '<div class="upload-icon">📁</div><div class="upload-text">点击上传xlsx分镜脚本</div>';
            updateQueueTable();
            addLog('队列已清空');
        });
        
        // 开始生成
        startBtn.addEventListener('click', async () => {
            const settings = {
                model: document.querySelector('#modelGroup .active').dataset.value,
                ratio: document.querySelector('#ratioGroup .active').dataset.value,
                resolution: document.querySelector('#resGroup .active').dataset.value,
                repeat: parseInt(document.querySelector('#repeatGroup .active').dataset.value)
            };
            
            startBtn.disabled = true;
            addLog('开始生成任务...');
            
            const response = await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ settings })
            });
        });
        
        // 更新队列表格
        function updateQueueTable() {
            const tbody = document.getElementById('queueBody');
            const pending = tasks.filter(t => t.status === 'pending').length;
            const done = tasks.filter(t => t.status === 'done').length;
            const total = tasks.length;
            
            document.getElementById('totalCount').textContent = total;
            document.getElementById('doneCount').textContent = done;
            document.getElementById('pendingCount').textContent = pending;
            document.getElementById('progressPercent').textContent = total ? Math.round(done/total*100) + '%' : '0%';
            document.getElementById('progressBar').style.width = (total ? done/total*100 : 0) + '%';
            document.getElementById('queueInfo').textContent = '共 ' + total + ' 个任务';
            
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#999;">请先上传xlsx文件</td></tr>';
                return;
            }
            
            tbody.innerHTML = tasks.map((t, i) => {
                const statusClass = 'status-' + t.status;
                const statusText = {pending:'等待',submitting:'提交中',generating:'生成中',done:'已完成',error:'错误'}[t.status] || t.status;
                const submitTime = t.submit_time ? t.submit_time.substring(11,19) : '-';
                const completeTime = t.complete_time ? t.complete_time.substring(11,19) : '-';
                const progress = t.status === 'done' ? '100%' : (t.status === 'generating' ? '50%' : '0%');
                
                return '<tr>' +
                    '<td>' + (i+1) + '</td>' +
                    '<td><span class="status-badge ' + statusClass + '">' + statusText + '</span></td>' +
                    '<td style="max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="' + t.prompt + '">' + t.prompt.substring(0,50) + '...</td>' +
                    '<td>' + submitTime + '</td>' +
                    '<td>' + completeTime + '</td>' +
                    '<td class="progress-cell"><div class="progress-mini"><div class="progress-mini-fill" style="width:' + progress + '"></div></div></td>' +
                '</tr>';
            }).join('');
        }
        
        function addLog(msg) {
            const logArea = document.getElementById('logArea');
            const time = new Date().toLocaleTimeString();
            logArea.textContent += '\\n[' + time + '] ' + msg;
            logArea.scrollTop = logArea.scrollHeight;
        }
        
        // 轮询状态
        setInterval(async () => {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.tasks && data.tasks.length > 0) {
                    tasks = data.tasks;
                    updateQueueTable();
                }
                
                if (data.log) {
                    document.getElementById('logArea').textContent = data.log;
                    document.getElementById('logArea').scrollTop = document.getElementById('logArea').scrollHeight;
                }
            } catch (e) {}
        }, 2000);
    </script>
</body>
</html>
'''

def parse_xlsx(filepath):
    """解析xlsx文件"""
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

日志 = []

def add_log(msg):
    日志.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(日志) > 50:
        日志.pop(0)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    global 状态, 日志
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file'})
    
    file = request.files['file']
    filepath = os.path.join('/tmp', 'upload_' + file.filename)
    file.save(filepath)
    
    try:
        prompts = parse_xlsx(filepath)
        repeat = 状态['settings']['repeat']
        
        # 创建任务列表
        状态['tasks'] = []
        task_id = 1
        for p in prompts:
            for _ in range(repeat):
                状态['tasks'].append({
                    'id': task_id,
                    'prompt': p,
                    'status': 'pending',
                    'submit_time': None,
                    'complete_time': None,
                    'error': None
                })
                task_id += 1
        
        add_log(f"已加载 {len(prompts)} 个提示词 × {repeat} 次 = {len(状态['tasks'])} 个任务")
        
        return jsonify({
            'success': True, 
            'tasks': 状态['tasks'],
            'count': len(状态['tasks'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/start', methods=['POST'])
def start():
    global 状态, 日志
    
    data = request.json
    状态['settings'] = data.get('settings', {})
    状态['is_running'] = True
    
    add_log(f"开始生成 - 模型:{状态['settings']['model']} 比例:{状态['settings']['ratio']} 分辨率:{状态['settings']['resolution']}")
    
    return jsonify({'success': True})

@app.route('/status', methods=['GET'])
def status():
    global 状态, 日志
    
    done = sum(1 for t in 状态['tasks'] if t['status'] == 'done')
    pending = sum(1 for t in 状态['tasks'] if t['status'] == 'pending')
    
    return jsonify({
        'is_running': 状态['is_running'],
        'tasks': 状态['tasks'],
        'total': len(状态['tasks']),
        'done': done,
        'pending': pending,
        'log': '\n'.join(日志)
    })

@app.route('/clear', methods=['POST'])
def clear():
    global 状态, 日志
    
    状态['tasks'] = []
    状态['is_running'] = False
    日志.clear()
    add_log("队列已清空")
    
    return jsonify({'success': True})

@app.route('/update_task', methods=['POST'])
def update_task():
    """更新任务状态"""
    global 状态
    
    data = request.json
    task_id = data.get('id')
    status = data.get('status')
    
    for task in 状态['tasks']:
        if task['id'] == task_id:
            task['status'] = status
            if status == 'submitting' or status == 'generating':
                task['submit_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            elif status == 'done':
                task['complete_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            break
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 启动即梦AI批量生成器 v3.0...")
    print("📍 访问地址: http://localhost:5001")
    print("📋 新增功能: 队列列表、实时进度追踪")
    app.run(host='0.0.0.0', port=5001, debug=False)
