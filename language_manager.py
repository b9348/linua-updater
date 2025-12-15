import os
import sys
import json
import locale

class LanguageManager:
    """语言管理器，负责检测系统语言和加载对应的语言资源"""
    
    def __init__(self):
        self.current_language = "en"  # 默认为英文
        self.translations = {}
        self.detect_system_language()
        self.load_language()
    
    def detect_system_language(self):
        """检测系统语言"""
        try:
            # 获取系统默认语言
            system_locale = locale.getdefaultlocale()
            if system_locale and system_locale[0]:
                lang_code = system_locale[0].lower()
                # 检查是否为中文（zh开头）
                if lang_code.startswith('zh'):
                    self.current_language = "zh"
                else:
                    self.current_language = "en"
            else:
                self.current_language = "en"
        except:
            # 如果检测失败，使用默认英文
            self.current_language = "en"
    
    def load_language(self):
        """加载语言资源文件"""
        try:
            # 获取语言文件路径
            if hasattr(sys, '_MEIPASS'):
                # 如果是打包后的exe环境
                lang_dir = os.path.join(sys._MEIPASS, 'lang')
            else:
                # 如果是开发环境
                current_dir = os.path.dirname(os.path.abspath(__file__))
                lang_dir = os.path.join(current_dir, "lang")
            
            lang_file = os.path.join(lang_dir, f"lang_{self.current_language}.json")
            
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
            else:
                # 如果找不到对应语言文件，尝试加载英文
                en_file = os.path.join(lang_dir, "lang_en.json")
                if os.path.exists(en_file):
                    with open(en_file, 'r', encoding='utf-8') as f:
                        self.translations = json.load(f)
                else:
                    # 如果连英文文件都没有，使用空字典
                    self.translations = {}
        except Exception as e:
            # 加载失败时使用空字典
            self.translations = {}
    
    def get(self, key, **kwargs):
        """获取翻译文本，支持格式化参数"""
        text = self.translations.get(key, key)  # 如果找不到翻译，返回key本身
        
        # 如果提供了格式化参数，进行格式化
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass  # 格式化失败时返回原始文本
        
        return text
    
    def set_language(self, lang_code):
        """手动设置语言"""
        if lang_code in ["en", "zh"]:
            self.current_language = lang_code
            self.load_language()
            return True
        return False
    
    def get_current_language(self):
        """获取当前语言代码"""
        return self.current_language