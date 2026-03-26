#!/usr/bin/env python3
"""
即梦AI批量图片生成器 v4.0 - Apple设计风格
支持AI生成描述词并迭代3次
"""
import os
import json
import time
import re
from flask import Flask, render_template_string, request, jsonify
import openpyxl
import threading
import time

app = Flask(__name__)
app.secret_key = 'jimeng-v4-secret-key'

# 全局状态
状态 = {
    'is_running': False,
    'tasks': [],
    'current_index': 0,
    'settings': {
        'model': '图片4.6',
        'ratio': '16:9',
        'resolution': '2K',
        'repeat': 1
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>即梦AI - 智能图片生成</title>
    <style>
        :root {
            --primary: #007AFF;
            --bg: #000000;
            --card: #1C1C1E;
            --card2: #2C2C2E;
            --text: #FFFFFF;
            --text2: #8E8E93;
            --green: #30D158;
            --orange: #FF9F0A;
            --red: #FF453A;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            line-height: 1.5;
        }
        .container { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
        
        /* Header */
        .header { text-align: center; margin-bottom: 50px; }
        .header h1 {
            font-size: 48px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #fff, #888);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p { color: var(--text2); font-size: 21px; font-weight: 400; }
        
        // 浏览器状态
        .browser-status {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            border: 2px solid var(--card2);
        }
        .browser-status.connected { border-color: var(--green); }
        .browser-status.working { border-color: var(--primary); animation: pulse 2s infinite; }
        .browser-status.disconnected { border-color: var(--orange); }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .browser-status h3 {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            font-size: 17px;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--orange);
            animation: blink 1s infinite;
        }
        .connected .status-dot { background: var(--green); animation: none; }
        .working .status-dot { background: var(--primary); animation: blink 0.5s infinite; }
        @keyframes blink { 50% { opacity: 0.3; } }
        .browser-steps {
            font-size: 14px;
            color: var(--text2);
            line-height: 1.8;
        }
        .browser-steps ol { margin-left: 20px; }
        .browser-steps a { color: var(--primary); }
        
        /* Cards */
        .card {
            background: var(--card);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
        }
        
        /* Upload Section */
        .upload-zone {
            border: 2px dashed var(--text2);
            border-radius: 16px;
            padding: 60px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-zone:hover { border-color: var(--primary); background: rgba(0,122,255,0.05); }
        .upload-icon { font-size: 48px; margin-bottom: 16px; }
        .upload-text { color: var(--text2); font-size: 17px; }
        input[type="file"] { display: none; }
        
        /* Settings Grid */
        .settings-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .setting-item { margin-bottom: 20px; }
        .setting-label { 
            color: var(--text2); 
            font-size: 13px; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
        
        /* Buttons */
        .btn-group { display: flex; gap: 12px; margin-top: 30px; }
        .btn {
            flex: 1;
            padding: 18px 32px;
            border-radius: 14px;
            font-size: 17px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: #0077ED; }
        .btn-primary:disabled { background: var(--card2); color: var(--text2); }
        .btn-secondary { background: var(--card2); color: var(--text); }
        .btn-danger { background: rgba(255,69,58,0.2); color: var(--red); }
        
        /* Select Pills */
        .pills { display: flex; flex-wrap: wrap; gap: 10px; }
        .pill {
            padding: 10px 20px;
            background: var(--card2);
            border-radius: 10px;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
        }
        .pill:hover { background: #3A3A3C; }
        .pill.active { background: var(--primary); border-color: var(--primary); }
        
        /* Stats */
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 30px 0; }
        .stat-box {
            background: var(--card);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
        }
        .stat-num { font-size: 36px; font-weight: 700; color: var(--primary); }
        .stat-label { color: var(--text2); font-size: 13px; margin-top: 4px; }
        
        /* Progress */
        .progress-track {
            height: 8px;
            background: var(--card2);
            border-radius: 4px;
            overflow: hidden;
            margin: 20px 0;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--green));
            width: 0%;
            transition: width 0.5s ease;
        }
        
        /* Table */
        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; }
        th {
            text-align: left;
            padding: 16px;
            color: var(--text2);
            font-size: 13px;
            font-weight: 600;
            border-bottom: 1px solid var(--card2);
        }
        td { padding: 16px; border-bottom: 1px solid var(--card2); font-size: 14px; }
        tr:hover { background: rgba(255,255,255,0.02); }
        
        /* Status Badge */
        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
        }
        .status-pending { background: var(--card2); color: var(--text2); }
        .status-iterating { background: rgba(255,159,10,0.2); color: var(--orange); }
        .status-submitting { background: rgba(0,122,255,0.2); color: var(--primary); }
        .status-generating { background: rgba(48,209,88,0.2); color: var(--green); }
        .status-done { background: rgba(48,209,88,0.2); color: var(--green); }
        
        /* Log */
        .log {
            background: #1C1C1E;
            border-radius: 12px;
            padding: 16px;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 12px;
            color: var(--green);
            max-height: 120px;
            overflow-y: auto;
        }
        
        /* AI Prompt Section */
        .ai-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
        }
        .ai-section h2 { 
            font-size: 24px; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ai-input {
            width: 100%;
            background: var(--card);
            border: none;
            border-radius: 12px;
            padding: 16px;
            color: var(--text);
            font-size: 16px;
            margin-bottom: 16px;
        }
        .ai-input:focus { outline: 2px solid var(--primary); }
        .iteration-tag {
            display: inline-block;
            padding: 4px 10px;
            background: var(--primary);
            border-radius: 12px;
            font-size: 12px;
            margin-right: 8px;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 32px; }
            .stats { grid-template-columns: repeat(2, 1fr); }
            .settings-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ 即梦AI</h1>
            <p>智能图片批量生成器</p>
        </div>
        
        <!-- 即梦进度监控 -->
        <div class="card" id="jimengProgress" style="display:none;">
            <h3>📊 即梦AI生成进度</h3>
            <div id="jimengTaskList"></div>
        </div>
        
        <!-- 浏览器状态 -->
        <div class="browser-status disconnected" id="browserStatus">
            <h3><span class="status-dot"></span> <span id="browserStatusText">浏览器未连接</span></h3>
            <div id="browserSteps">
                <span style="color:var(--text2);">请先完成以下步骤：</span>
                <ol style="margin-left:20px;color:var(--text2);font-size:14px;line-height:1.8;">
                    <li>打开Chrome浏览器，访问 <a href="https://jimeng.jianying.com/ai-tool/generate/?type=image" target="_blank" style="color:var(--primary);">即梦AI图片生成页面</a></li>
                    <li>点击浏览器右上角的OpenClaw扩展图标</li>
                    <li>等待显示"连接成功"</li>
                </ol>
                <button class="btn" style="background:#28a745;color:white;margin-top:10px;" id="autoFixBtn" onclick="autoFix()">🔧 一键修复/连接</button>
                <button class="btn btn-secondary" id="autoConnectBtn" style="margin-top:15px;display:none;width:100%;" onclick="doAutoConnect()">🤖 自动打开Chrome和即梦AI</button>
            </div>
        </div>
        
        <!-- AI生成描述词 -->
        <div class="ai-section">
            <h2>🤖 AI生成描述词 <span style="font-size:14px;color:var(--text2);font-weight:400;">(迭代3次优化)</span></h2>
            <input type="text" class="ai-input" id="aiPrompt" placeholder="输入你想要生成图片的主题，例如：一只在海边玩耍的金毛狗狗">
            <div class="btn-group">
                <button class="btn btn-primary" id="generateBtn" onclick="generatePrompt()">生成描述词</button>
            </div>
            <div id="aiResult" style="margin-top:20px;"></div>
        </div>
        
        <!-- 上传文件 -->
        <div class="card">
            <h2 style="margin-bottom:20px;font-size:24px;">📁 上传分镜脚本</h2>
            <div class="upload-zone" id="uploadZone">
                <div class="upload-icon">📤</div>
                <div class="upload-text">点击或拖拽上传 xlsx 分镜脚本</div>
                <input type="file" id="fileInput" accept=".xlsx">
            </div>
            <div id="fileInfo" style="margin-top:16px;color:var(--text2);"></div>
        </div>
        
        <!-- 设置 -->
        <div class="card">
            <h2 style="margin-bottom:24px;font-size:24px;">⚙️ 生成设置</h2>
            <div class="settings-grid">
                <div class="setting-item">
                    <div class="setting-label">生图模型</div>
                    <div class="pills" id="modelPills">
                        <div class="pill active" data-value="图片4.6">图片4.6</div>
                        <div class="pill" data-value="图片5.0 Lite">图片5.0 Lite</div>
                        <div class="pill" data-value="图片3.0">图片3.0</div>
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-label">画面比例</div>
                    <div class="pills" id="ratioPills">
                        <div class="pill active" data-value="16:9">16:9</div>
                        <div class="pill" data-value="智能">智能</div>
                        <div class="pill" data-value="3:2">3:2</div>
                        <div class="pill" data-value="1:1">1:1</div>
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-label">分辨率</div>
                    <div class="pills" id="resPills">
                        <div class="pill active" data-value="2K">2K</div>
                        <div class="pill" data-value="4K">4K</div>
                        <div class="pill" data-value="高清">高清</div>
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-label">生成次数</div>
                    <div class="pills" id="repeatPills">
                        <div class="pill active" data-value="1">1次</div>
                        <div class="pill" data-value="3">3次</div>
                        <div class="pill" data-value="4">4次</div>
                    </div>
                </div>
            </div>
            
            <div class="btn-group">
                <button class="btn btn-primary" id="startBtn" disabled>开始生成</button>
                <button class="btn btn-secondary" id="optimizeBtn" onclick="optimizePrompts()">✨ 一键优化提示词</button>
                <button class="btn btn-danger" onclick="clearQueue()">清空队列</button>
            </div>
        </div>
        
        <!-- 统计 -->
        <div class="stats">
            <div class="stat-box">
                <div class="stat-num" id="totalCount">0</div>
                <div class="stat-label">总任务数</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" id="doneCount">0</div>
                <div class="stat-label">已完成</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" id="iterCount">0</div>
                <div class="stat-label">迭代中</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" id="percent">0%</div>
                <div class="stat-label">进度</div>
            </div>
        </div>
        
        <div class="progress-track">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        
        <!-- 任务列表 -->
        <div class="card">
            <h2 style="margin-bottom:24px;font-size:24px;">📋 任务队列</h2>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>状态</th>
                            <th>描述词</th>
                            <th>迭代</th>
                            <th>时间</th>
                        </tr>
                    </thead>
                    <tbody id="taskBody">
                        <tr><td colspan="5" style="text-align:center;color:var(--text2);padding:40px;">请上传xlsx文件或生成描述词</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 日志 -->
        <div class="log" id="logArea">等待操作...</div>
    </div>
    
    <script>
        let tasks = [];
        let aiIterations = [];
        
        // Pill选择
        document.querySelectorAll('.pills').forEach(pills => {
            pills.querySelectorAll('.pill').forEach(pill => {
                pill.addEventListener('click', () => {
                    pills.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
                    pill.classList.add('active');
                });
            });
        });
        
        // 上传
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const startBtn = document.getElementById('startBtn');
        
        // 点击上传
        uploadZone.addEventListener('click', () => fileInput.click());
        
        // 拖拽上传
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'var(--primary)';
            uploadZone.style.background = 'rgba(0,122,255,0.1)';
        });
        
        uploadZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'var(--text2)';
            uploadZone.style.background = 'transparent';
        });
        
        uploadZone.addEventListener('drop', async (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'var(--text2)';
            uploadZone.style.background = 'transparent';
            
            const file = e.dataTransfer.files[0];
            if (!file || !file.name.endsWith('.xlsx')) {
                alert('请上传xlsx文件');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            uploadZone.innerHTML = '<div class="upload-icon">⏳</div><div class="upload-text">解析中...</div>';
            
            try {
                const response = await fetch('/upload', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.success) {
                    tasks = data.tasks;
                    uploadZone.innerHTML = '<div class="upload-icon">✅</div><div class="upload-text">已加载 ' + tasks.length + ' 个任务</div>';
                    document.getElementById('fileInfo').textContent = '文件: ' + file.name;
                    startBtn.disabled = false;
                    updateUI();
                    addLog('已加载 ' + tasks.length + ' 个任务');
                }
            } catch (err) {
                uploadZone.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">错误</div>';
            }
        });
        
        // 文件选择上传
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            uploadZone.innerHTML = '<div class="upload-icon">⏳</div><div class="upload-text">解析中...</div>';
            
            try {
                const response = await fetch('/upload', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.success) {
                    tasks = data.tasks;
                    uploadZone.innerHTML = '<div class="upload-icon">✅</div><div class="upload-text">已加载 ' + tasks.length + ' 个任务</div>';
                    document.getElementById('fileInfo').textContent = '文件: ' + file.name;
                    startBtn.disabled = false;
                    updateUI();
                    addLog('已加载 ' + tasks.length + ' 个任务');
                }
            } catch (err) {
                uploadZone.innerHTML = '<div class="upload-icon">❌</div><div class="upload-text">错误</div>';
            }
        });
        
        // AI生成描述词
        async function generatePrompt() {
            const input = document.getElementById('aiPrompt').value.trim();
            if (!input) { alert('请输入主题'); return; }
            
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.textContent = '生成中...';
            
            try {
                const response = await fetch('/ai_generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: input})
                });
                const data = await response.json();
                
                if (data.success) {
                    aiIterations = data.iterations;
                    displayAIResult(data.iterations);
                    addLog('AI生成了 ' + data.iterations.length + ' 个描述词');
                }
            } catch (err) {
                alert('生成失败: ' + err.message);
            }
            
            btn.disabled = false;
            btn.textContent = '生成描述词';
        }
        
        function displayAIResult(iterations) {
            const container = document.getElementById('aiResult');
            container.innerHTML = iterations.map((item, i) => `
                <div style="background:var(--card);border-radius:12px;padding:20px;margin-bottom:12px;">
                    <div style="display:flex;align-items:center;margin-bottom:10px;">
                        <span class="iteration-tag">迭代 ${i + 1}</span>
                        <span style="color:var(--text2);font-size:13px;">${item.time}</span>
                    </div>
                    <p style="font-size:16px;line-height:1.6;">${item.prompt}</p>
                </div>
            `).join('');
            
            // 添加到任务队列
            tasks = iterations.map((item, i) => ({
                id: i + 1,
                prompt: item.prompt,
                status: 'pending',
                iteration: i + 1,
                submit_time: '',
                complete_time: ''
            }));
            
            startBtn.disabled = false;
            updateUI();
        }
        
        // 清空
        async function clearQueue() {
            try {
                await fetch('/clear', { method: 'POST' });
            } catch (e) {}
            tasks = [];
            startBtn.disabled = true;
            uploadZone.innerHTML = '<div class="upload-icon">📤</div><div class="upload-text">点击或拖拽上传 xlsx 分镜脚本</div>';
            document.getElementById('fileInfo').textContent = '';
            document.getElementById('aiResult').innerHTML = '';
            updateUI();
            addLog('队列已清空');
        }
        
        // 开始生成
        startBtn.addEventListener('click', async () => {
            const settings = {
                model: document.querySelector('#modelPills .active').dataset.value,
                ratio: document.querySelector('#ratioPills .active').dataset.value,
                resolution: document.querySelector('#resPills .active').dataset.value,
                repeat: parseInt(document.querySelector('#repeatPills .active').dataset.value)
            };
            
            startBtn.disabled = true;
            addLog('开始生成...');
            
            await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({settings, tasks})
            });
            
            // 立即提交第一个任务
            const firstPending = tasks.find(t => t.status === 'pending');
            if (firstPending) {
                addLog('立即提交: ' + firstPending.prompt.substring(0,30) + '...');
                await fetch('/auto_submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: firstPending.prompt, settings: settings})
                });
                firstPending.status = 'submitting';
                firstPending.submit_time = new Date().toLocaleTimeString();
                updateUI();
            }
        });
        
        // 更新UI
        function updateUI() {
            const total = tasks.length;
            const done = tasks.filter(t => t.status === 'done').length;
            const iter = tasks.filter(t => t.status === 'iterating').length;
            const percent = total ? Math.round(done/total*100) : 0;
            
            document.getElementById('totalCount').textContent = total;
            document.getElementById('doneCount').textContent = done;
            document.getElementById('iterCount').textContent = iter;
            document.getElementById('percent').textContent = percent + '%';
            document.getElementById('progressBar').style.width = percent + '%';
            
            const tbody = document.getElementById('taskBody');
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text2);padding:40px;">请上传xlsx文件或生成描述词</td></tr>';
                return;
            }
            
            tbody.innerHTML = tasks.map((t, i) => {
                const statusClass = 'status-' + t.status;
                const statusText = {pending:'等待',iterating:'迭代中',submitting:'提交',generating:'生成',done:'完成'}[t.status] || t.status;
                const iterTag = t.iteration ? `<span class="iteration-tag">V${t.iteration}</span>` : '';
                const time = t.complete_time || t.submit_time || '-';
                
                return '<tr>' +
                    '<td>' + (i+1) + '</td>' +
                    '<td><span class="status ' + statusClass + '">' + statusText + '</span></td>' +
                    '<td style="max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + iterTag + t.prompt.substring(0,50) + '...</td>' +
                    '<td>' + (t.iteration || '-') + '</td>' +
                    '<td style="color:var(--text2);font-size:13px;">' + time + '</td>' +
                '</tr>';
            }).join('');
        }
        
        // 自动连接浏览器
        async function doAutoConnect() {
            const btn = document.getElementById("autoConnectBtn");
            btn.disabled = true;
            btn.textContent = "⏳ 正在打开Chrome...";
            
            try {
                const res = await fetch("/auto_connect", { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    btn.textContent = "✅ 已打开Chrome，请点击OpenClaw扩展图标连接";
                    addLog("自动打开Chrome成功，请在Chrome中点击OpenClaw扩展图标");
                    setTimeout(() => location.reload(), 5000);
                } else {
                    btn.textContent = "❌ " + data.message;
                }
            } catch (e) {
                btn.textContent = "❌ 连接失败";
            }
            
            btn.disabled = false;
        }
        
        function addLog(msg) {
            const logArea = document.getElementById('logArea');
            const time = new Date().toLocaleTimeString();
            logArea.textContent += '\\n[' + time + '] ' + msg;
            logArea.scrollTop = logArea.scrollHeight;
        }
        
                // 一键优化提示词
        async function optimizePrompts() {
            const subject = prompt('请输入主体描述（例如：一只金毛狗狗/模特穿某款衣服）', '主角');
            if (!subject) return;
            
            const btn = document.getElementById('optimizeBtn');
            btn.disabled = true;
            btn.textContent = '优化中...';
            
            try {
                const res = await fetch('/optimize_prompts', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompts: tasks.map(t => t.prompt), subject: subject})
                });
                const data = await res.json();
                
                if (data.success) {
                    // Update tasks with optimized prompts
                    tasks = data.optimized.map((p, i) => ({
                        id: i + 1,
                        prompt: p,
                        status: 'pending',
                        submit_time: '',
                        complete_time: ''
                    }));
                    updateUI();
                    addLog('已优化 ' + tasks.length + ' 个提示词');
                }
            } catch (e) {
                alert('优化失败: ' + e.message);
            }
            
            btn.disabled = false;
            btn.textContent = '✨ 一键优化提示词';
        }
        
                // 一键修复 - 自动打开浏览器和即梦
        async function autoFix() {
            const btn = document.getElementById('autoFixBtn');
            btn.disabled = true;
            btn.textContent = '🔧 修复中...';
            
            try {
                const res = await fetch('/auto_connect', { method: 'POST' });
                const data = await res.json();
                
                if (data.success) {
                    btn.textContent = '✅ 已修复';
                    setTimeout(() => location.reload(), 3000);
                } else {
                    btn.textContent = '❌ ' + data.message;
                }
            } catch (e) {
                btn.textContent = '❌ 失败';
            }
            
            btn.disabled = false;
        }
        
        // 轮询 - 每3秒检查即梦进度
        async function checkJimengProgress() {
            try {
                const res = await fetch('/check_jimeng');
                const data = await res.json();
                
                const progressDiv = document.getElementById('jimengProgress');
                const taskList = document.getElementById('jimengTaskList');
                
                if (data.tasks && data.tasks.length > 0) {
                    progressDiv.style.display = 'block';
                    taskList.innerHTML = data.tasks.map(t => 
                        '<div style="padding:8px;background:var(--card2);border-radius:8px;margin-bottom:8px;">⏳ ' + t.substring(0,30) + '...</div>'
                    ).join('');
                } else {
                    progressDiv.style.display = 'none';
                }
            } catch (e) {}
        }
        
                // 一键修复 - 自动打开浏览器和即梦
        async function autoFix() {
            const btn = document.getElementById('autoFixBtn');
            btn.disabled = true;
            btn.textContent = '🔧 修复中...';
            
            try {
                const res = await fetch('/auto_connect', { method: 'POST' });
                const data = await res.json();
                
                if (data.success) {
                    btn.textContent = '✅ 已修复';
                    setTimeout(() => location.reload(), 3000);
                } else {
                    btn.textContent = '❌ ' + data.message;
                }
            } catch (e) {
                btn.textContent = '❌ 失败';
            }
            
            btn.disabled = false;
        }
        
        // 轮询 - 每3秒检查状态
        setInterval(async () => {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                if (data.tasks && data.tasks.length > 0) {
                    tasks = data.tasks;
                    updateUI();
                    
                    // 自动提交任务
                    const pendingTask = tasks.find(t => t.status === 'pending');
                    if (pendingTask && browserData.connected) {
                        // 提交到即梦
                        await fetch('/auto_submit', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({prompt: pendingTask.prompt})
                        });
                        // 更新任务状态
                        pendingTask.status = 'submitting';
                        pendingTask.submit_time = new Date().toLocaleTimeString();
                        updateUI();
                    }
                }
                if (data.log) {
                    document.getElementById('logArea').textContent = data.log;
                }
                
                // 检查浏览器状态和即梦工作状态
                const browserRes = await fetch('/check_browser');
                const browserData = await browserRes.json();
                
                // 如果未连接，显示自动连接按钮
                const autoConnectBtn = document.getElementById('autoConnectBtn');
                if (!browserData.connected && autoConnectBtn) {
                    autoConnectBtn.style.display = 'inline-block';
                }
                
                // 检查即梦AI生成状态
                const statusEl = document.getElementById('browserStatus');
                const statusText = document.getElementById('browserStatusText');
                
                // 检查即梦AI生成状态
                const jimengRes = await fetch('/check_jimeng');
                const jimengData = await jimengRes.json();
                
                if (jimengData.has_tasks) {
                    statusEl.className = 'browser-status working';
                    statusText.textContent = '🎨 正在生成图片 (' + jimengData.task_count + '个任务)';
                    document.getElementById('browserSteps').innerHTML = '<span style="color:var(--primary);">⏳ 即梦AI正在工作中，请稍候...</span>';
                } else if (browserData.connected) {
                    statusEl.className = 'browser-status connected';
                    statusText.textContent = '✅ 浏览器已连接即梦AI';
                    document.getElementById('browserSteps').innerHTML = '<span style="color:var(--green);">🎉 可以开始生成图片了！</span>';
                } else {
                    statusEl.className = 'browser-status disconnected';
                    statusText.textContent = '⚠️ 浏览器未连接';
                }
            } catch (e) {}
            
            // 检查即梦进度
            checkJimengProgress();
        }, 3000);
    </script>
</body>
</html>
'''

def parse_xlsx(filepath):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    prompts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        if row[0] and isinstance(row[0], int) and row[1]:
            prompts.append(str(row[1]))
    return prompts

日志 = []

def add_log(msg):
    日志.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(日志) > 50:
        日志.pop(0)

# AI生成描述词的简单模拟（实际可以用API）
def generate_prompt_iterations(original_prompt):
    """生成3次迭代的描述词"""
    iterations = []
    
    # 迭代1: 详细描述
    v1 = f"{original_prompt}，高清画质，专业摄影布光，细节丰富，画面干净整洁，主体突出，背景虚化"
    iterations.append({"prompt": v1, "time": time.strftime('%H:%M:%S'), "version": 1})
    
    # 迭代2: 添加风格
    v2 = f"{original_prompt}，电影级质感，柔和自然光，浅景深，氛围感强，色调温暖，8K超清"
    iterations.append({"prompt": v2, "time": time.strftime('%H:%M:%S'), "version": 2})
    
    # 迭代3: 优化
    v3 = f"{original_prompt}，专业商业摄影风格，精致细节，完美构图，视觉冲击力强，高品质"
    iterations.append({"prompt": v3, "time": time.strftime('%H:%M:%S'), "version": 3})
    
    return iterations

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
        
        状态['tasks'] = []
        task_id = 1
        for p in prompts:
            for _ in range(repeat):
                状态['tasks'].append({
                    'id': task_id,
                    'prompt': p,
                    'status': 'pending',
                    'iteration': 1,
                    'submit_time': '',
                    'complete_time': ''
                })
                task_id += 1
        
        add_log(f"已加载 {len(prompts)} × {repeat} = {len(状态['tasks'])} 个任务")
        
        # 自动开始生成
        task_count = len(状态['tasks'])
        状态['is_running'] = True
        
        # 在后台启动自动提交
        threading.Thread(target=auto_submit_worker, daemon=True).start()
        
        # 发送飞书通知
        try:
            send_feishu_message(f"📤 已上传xlsx文件\n✅ 自动开始生成 {task_count} 个任务\n🎨 正在提交到即梦AI...")
        except Exception as e:
            add_log(f"飞书通知失败: {e}")
        
        return jsonify({'success': True, 'tasks': 状态['tasks'], 'auto_started': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def send_feishu_message(message):
    """发送飞书消息给用户 - 尝试多种方式"""
    import subprocess
    import sys
    
    # 方法1: 使用subprocess调用openclaw message
    try:
        result = subprocess.run(
            ['openclaw', 'message', 'send', 
             '--channel', 'feishu', 
             '--account', 'huangwenyu',
             '--target', 'user:ou_a5d1b3dd2d9ce52897c6b3d9b47c5786',
             '--message', message],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, 'HOME': os.environ.get('HOME', '/Users/poposhijue')}
        )
        if result.returncode == 0:
            add_log(f"飞书消息发送成功")
            return True
        else:
            add_log(f"飞书消息失败: {result.stderr}")
    except Exception as e:
        add_log(f"飞书消息异常: {e}")
    
    return False


@app.route('/optimize_prompts', methods=['POST'])
def optimize_prompts():
    """一键优化提示词，保持一致性"""
    global 状态
    data = request.json
    prompts = data.get('prompts', [])
    subject = data.get('subject', '主角')  # 主体描述
    
    if not prompts:
        return jsonify({'success': False, 'error': 'No prompts'})
    
    # 优化每个提示词
    optimized = []
    for i, p in enumerate(prompts):
        if i == 0:
            # 第一个提示词，添加主体描述
            new_p = f"{subject}，{p}，高清专业摄影，干净背景，细节丰富"
        else:
            # 后续提示词，添加与前一个提示词的关联
            new_p = f"接上一镜头，{subject}，{p}，与上一镜头风格一致，色调统一"
        optimized.append(new_p)
    
    add_log(f'已优化 {len(optimized)} 个提示词')
    return jsonify({'success': True, 'optimized': optimized})


@app.route('/analyze_prompts', methods=['POST'])
def analyze_prompts():
    """AI分析并优化提示词"""
    import httpx
    
    data = request.json
    prompts = data.get('prompts', [])
    
    if not prompts:
        return jsonify({'success': False, 'error': 'No prompts'})
    
    # 构建分析提示
    prompt_text = f"""请分析以下{len(prompts)}个视频分镜脚本，提取关键信息并优化每个提示词。

要求：
1. 提取主体（产品/主角）
2. 提取角色描述（性别、服装、外貌）
3. 提取场景风格（色调、光线、氛围）
4. 优化每个提示词，使其更详细具体，保持镜头间连贯

脚本内容：
{chr(10).join([f"镜头{i+1}: {p}" for i, p in enumerate(prompts)])}

请按以下格式输出：
---
主体: <提取的主体>
角色: <提取的角色描述>
风格: <提取的风格要求>
---
优化后的提示词:
{chr(10).join([f"{i+1}. {p}" for i, p in enumerate(prompts)])}
---
"""

    try:
        response = httpx.post(
            "https://api.minimax.chat/v1/text/chatcompletion_pro",
            headers={"Authorization": "Bearer $FASGA", "Content-Type": "application/json"},
            json={"model": "MiniMax-M2.5", "messages": [
                {"role": "system", "content": "你是专业的视频脚本分析优化专家"},
                {"role": "user", "content": prompt_text}
            ], "temperature": 0.7},
            timeout=60.0
        )
        
        result = response.json()
        ai_response = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # 解析AI响应
        lines = ai_response.split('\n')
        analysis = {'subject': '', 'character': '', 'style': ''}
        optimized = []
        in_optimized = False
        
        for line in lines:
            line = line.strip()
            if '主体:' in line:
                analysis['subject'] = line.replace('主体:', '').strip()
            elif '角色:' in line:
                analysis['character'] = line.replace('角色:', '').strip()
            elif '风格:' in line:
                analysis['style'] = line.replace('风格:', '').strip()
            elif '优化后的提示词' in line or in_optimized:
                in_optimized = True
                if line and not line.startswith('---'):
                    # 去掉编号
                    clean = line.lstrip('0123456789. ')
                    if clean:
                        optimized.append(clean)
        
        # 如果解析失败，使用原提示词
        if len(optimized) < len(prompts):
            optimized = prompts
        
        add_log(f'AI分析了 {len(prompts)} 个脚本')
        return jsonify({
            'success': True, 
            'analysis': analysis,
            'optimized': optimized
        })
        
    except Exception as e:
        add_log(f'AI分析失败: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/ai_generate', methods=['POST'])
def ai_generate():
    """AI生成描述词"""
    global 日志
    data = request.json
    original = data.get('prompt', '')
    
    if not original:
        return jsonify({'success': False, 'error': '请输入主题'})
    
    # 生成3次迭代
    iterations = generate_prompt_iterations(original)
    
    add_log(f"AI生成: {original[:20]}... → 3个迭代版本")
    
    return jsonify({
        'success': True,
        'iterations': iterations
    })

@app.route('/start', methods=['POST'])
def start():
    global 状态, 日志
    data = request.json
    状态['settings'] = data.get('settings', {})
    状态['tasks'] = data.get('tasks', [])
    状态['is_running'] = True
    
    add_log(f"开始 - 模型:{状态.get('settings', {}).get('model', '图片4.6')} 比例:{状态.get('settings', {}).get('ratio', '16:9')}")
    
    return jsonify({'success': True})

@app.route('/clear', methods=['POST'])
def clear_queue():
    """清空队列"""
    global 状态, 日志
    状态['tasks'] = []
    状态['is_running'] = False
    日志 = []
    add_log('队列已清空')
    return jsonify({'success': True})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'is_running': 状态['is_running'],
        'tasks': 状态['tasks'],
        'total': len(状态['tasks']),
        'done': sum(1 for t in 状态['tasks'] if t['status'] == 'done'),
        'log': '\n'.join(日志)
    })

@app.route('/check_browser', methods=['GET'])
def check_browser():
    """检查浏览器是否连接即梦AI"""
    import subprocess
    try:
        # 尝试启动浏览器
        subprocess.run(['openclaw', 'browser', 'start', '--profile', 'chrome'], capture_output=True, timeout=10)
        
        result = subprocess.run(
            ['openclaw', 'browser', 'tabs', '--profile', 'chrome'],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout
        
        # 检查是否有即梦AI页面
        has_jimeng = 'jimeng' in output.lower() or '即梦' in output
        
        # 如果没有即梦页面，尝试打开
        if not has_jimeng:
            subprocess.run(
                ['openclaw', 'browser', 'open', 'https://jimeng.jianying.com/ai-tool/generate/?type=image', '--profile', 'chrome'],
                capture_output=True, timeout=15
            )
            has_jimeng = True
        
        # 检查是否有多个标签（表示已连接）
        tab_count = output.count('id:')
        
        return jsonify({
            'connected': has_jimeng and tab_count > 0, 
            'has_jimeng': has_jimeng,
            'tab_count': tab_count,
            'message': '已连接即梦AI' if (has_jimeng and tab_count > 0) else '未连接到即梦AI'
        })
    except Exception as e:
        return jsonify({'connected': False, 'message': str(e)})

@app.route('/auto_connect', methods=['POST'])
def auto_connect():
    """自动打开Chrome并连接到即梦AI"""
    import subprocess
    import time
    
    try:
        # 先停止现有浏览器
        subprocess.run(['openclaw', 'browser', 'stop', '--profile', 'chrome'], capture_output=True)
        time.sleep(1)
        
        # 启动浏览器（使用OpenClaw自己的浏览器驱动）
        subprocess.run(['openclaw', 'browser', 'start', '--profile', 'chrome'], capture_output=True)
        time.sleep(2)
        
        # 使用OpenClaw打开即梦AI页面
        result = subprocess.run(
            ['openclaw', 'browser', 'open', 'https://jimeng.jianying.com/ai-tool/generate/?type=image', '--profile', 'chrome'],
            capture_output=True, text=True, timeout=10
        )
        
        return jsonify({
            'success': True, 
            'message': '✅ 已自动启动浏览器并打开即梦AI，请刷新页面确认连接状态'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/check_jimeng', methods=['GET'])

def check_jimeng():
    """检查即梦AI是否有正在生成的任务"""
    import subprocess
    try:
        result = subprocess.run(
            ['openclaw', 'browser', 'snapshot', '--profile', 'chrome'],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout
        
        # 检查是否有"生成中"或"造梦"等关键词
        has_tasks = '生成中' in output or '造梦' in output or '智能创意' in output
        
        # 统计任务数量
        task_count = output.count('生成中')
        
        return jsonify({
            'has_tasks': has_tasks,
            'task_count': task_count,
            'status': 'working' if has_tasks else 'idle'
        })
    except Exception as e:
        return jsonify({'has_tasks': False, 'task_count': 0, 'status': 'error', 'message': str(e)})

@app.route('/auto_submit', methods=['POST'])
def auto_submit():
    """自动提交任务到即梦AI"""
    global 状态, 日志
    
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'success': False, 'error': 'No prompt'})
    
    import subprocess
    
    try:
        # 使用JavaScript直接输入并提交（更可靠）
        js_code = f"var inp = document.querySelector('input[placeholder*=描述]'); if(inp) {{ inp.value = '{prompt}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); setTimeout(function(){{inp.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',bubbles:true}}));}},100); }}"
        
        result = subprocess.run(
            ['openclaw', 'browser', 'act', '--profile', 'chrome', '--request', '{"kind":"evaluate","fn":"' + js_code + '"}'],
            capture_output=True, text=True, timeout=15
        )
        
        add_log(f'已提交: {prompt[:30]}...')
        return jsonify({'success': True})
        
    except Exception as e:
        add_log(f'提交失败: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})



# 后台自动提交 worker
def auto_submit_worker():
    """后台自动提交任务到即梦AI"""
    global 状态
    last_prompt = ""
    
    while True:
        time.sleep(3)  # 每3秒检查一次
        if not 状态.get('is_running'):
            continue
        
        # 找pending任务
        pending = [t for t in 状态['tasks'] if t['status'] == 'pending']
        if not pending:
            continue
        
        task = pending[0]
        
        # 如果跟上次一样，说明正在生成，跳过
        if task['prompt'] == last_prompt:
            continue
        
        task['status'] = 'submitting'
        prompt = task['prompt']
        
        try:
            # 发送HTTP请求到本地agent来控制浏览器
            import requests
            try:
                # 获取当前输入框元素
                r = requests.get('http://127.0.0.1:5001/browser_snapshot', timeout=5)
                # 简单方式：直接用JavaScript
            except:
                pass
            
            # 使用subprocess调用browser act
            import subprocess
            
            # 输入提示词 - 使用JavaScript直接操作
            js_code = f"var inp = document.querySelector('input[placeholder*=描述]'); if(inp) {{ inp.value = '{prompt}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); setTimeout(function(){{inp.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',bubbles:true}}));}},500); }}"
            
            result = subprocess.run(
                ['openclaw', 'browser', 'act', '--profile', 'chrome', 
                 '--request', '{"kind":"evaluate","fn":"' + js_code + '"}'],
                capture_output=True, text=True, timeout=20
            )
            
            last_prompt = prompt
            task['submit_time'] = time.strftime('%H:%M:%S')
            add_log(f'已提交: {prompt[:30]}...')
        except Exception as e:
            add_log(f'提交失败: {str(e)}')
            task['status'] = 'pending'

# 启动后台worker
worker_thread = threading.Thread(target=auto_submit_worker, daemon=True)
worker_thread.start()

def fast_submit_task():
    """极速提交任务"""
    import subprocess
    pending = [t for t in 状态['tasks'] if t['status'] == 'pending']
    if not pending:
        return
    
    task = pending[0]
    task['status'] = 'submitting'
    
    try:
        result = subprocess.run(
            ['python3', '/Users/poposhijue/.openclaw/workspace/skills/jimeng-auto-generator/stable_submit.py', task['prompt']],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            add_log(f'极速提交: {task["prompt"][:30]}...')
        else:
            add_log(f'提交失败: {result.stderr}')
            task['status'] = 'pending'
    except Exception as e:
        add_log(f'提交异常: {str(e)}')
        task['status'] = 'pending'

# 极速提交worker
def fast_worker():
    while True:
        time.sleep(1)  # 每1秒检查一次
        if 状态.get('is_running'):
            fast_submit_task()

import threading
fast_thread = threading.Thread(target=fast_worker, daemon=True)
fast_thread.start()

if __name__ == '__main__':
    print("🚀 即梦AI v4.0 - Apple设计风格")
    print("📍 http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
