#!/usr/bin/env python3
"""
Code Review Tool Module - Code Quality Analysis

Provides code review capabilities to analyze code quality, identify potential issues,
and suggest improvements. Uses static analysis to detect common problems and best
practice violations.

Design:
- Single `code_review` tool: analyze code files or directories
- Returns detailed analysis with issues and recommendations
- Supports multiple programming languages
- Integrates with existing codebase structure
"""

import json
import os
import re
from typing import Dict, Any, List, Optional

from tools.registry import registry, tool_error


class CodeReviewer:
    """
    Code reviewer that analyzes code quality and identifies issues.
    """

    def __init__(self):
        # Common patterns for different languages
        self.language_patterns = {
            'python': {
                'extension': '.py',
                'shebang': r'^#!/usr/bin/env python',
                'imports': r'^import\s+|^from\s+.*import\s+',
                'docstring': r'"""[\s\S]*?"""',
                'function': r'def\s+\w+\s*\([^)]*\):',
                'class': r'class\s+\w+\s*\([^)]*\):',
                'comment': r'#.*$',
                'indentation': r'^\s+'
            },
            'javascript': {
                'extension': '.js',
                'shebang': r'^#!/usr/bin/env node',
                'imports': r'^import\s+|^const\s+.*=\s+require\(',
                'function': r'function\s+\w+\s*\(|const\s+\w+\s*=\s*\(.*\)\s*=>',
                'class': r'class\s+\w+\s*{',
                'comment': r'//.*$|/\*[\s\S]*?\*/',
                'indentation': r'^\s+'
            },
            'typescript': {
                'extension': '.ts',
                'shebang': r'^#!/usr/bin/env node',
                'imports': r'^import\s+|^const\s+.*=\s+require\(',
                'function': r'function\s+\w+\s*\(|const\s+\w+\s*=\s*\(.*\)\s*=>',
                'class': r'class\s+\w+\s*{',
                'comment': r'//.*$|/\*[\s\S]*?\*/',
                'indentation': r'^\s+'
            }
        }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single code file and return review results.
        """
        if not os.path.exists(file_path):
            return {
                'file': file_path,
                'error': 'File not found'
            }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file': file_path,
                'error': f'Error reading file: {str(e)}'
            }

        # Determine language based on file extension
        language = self._detect_language(file_path)
        if not language:
            return {
                'file': file_path,
                'error': 'Unsupported file type'
            }

        # Analyze code
        issues = self._analyze_content(content, language, file_path)
        metrics = self._calculate_metrics(content, language)

        return {
            'file': file_path,
            'language': language,
            'issues': issues,
            'metrics': metrics,
            'recommendations': self._generate_recommendations(issues, metrics)
        }

    def analyze_directory(self, directory: str) -> List[Dict[str, Any]]:
        """
        Analyze all code files in a directory and return review results.
        """
        if not os.path.exists(directory):
            return [{
                'error': 'Directory not found'
            }]

        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_supported_file(file):
                    results.append(self.analyze_file(file_path))
        return results

    def _detect_language(self, file_path: str) -> Optional[str]:
        """
        Detect programming language based on file extension.
        """
        extension = os.path.splitext(file_path)[1]
        for lang, patterns in self.language_patterns.items():
            if extension == patterns['extension']:
                return lang
        return None

    def _is_supported_file(self, file_name: str) -> bool:
        """
        Check if the file is supported for analysis.
        """
        extension = os.path.splitext(file_name)[1]
        for patterns in self.language_patterns.values():
            if extension == patterns['extension']:
                return True
        return False

    def _analyze_content(self, content: str, language: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Analyze code content for issues.
        """
        issues = []
        lines = content.split('\n')

        # Check for common issues
        issues.extend(self._check_indentation(lines, language))
        issues.extend(self._check_line_length(lines))
        issues.extend(self._check_empty_lines(lines))
        issues.extend(self._check_comments(lines, language))
        issues.extend(self._check_naming_conventions(lines, language))

        return issues

    def _check_indentation(self, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """
        Check for indentation issues.
        """
        issues = []
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith('\t') and not line.startswith('    '):
                issues.append({
                    'line': i,
                    'type': 'indentation',
                    'severity': 'warning',
                    'message': 'Inconsistent indentation'
                })
        return issues

    def _check_line_length(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Check for lines that are too long.
        """
        issues = []
        for i, line in enumerate(lines, 1):
            if len(line) > 88:  # PEP 8 recommendation
                issues.append({
                    'line': i,
                    'type': 'line_length',
                    'severity': 'warning',
                    'message': f'Line too long ({len(line)} characters)'
                })
        return issues

    def _check_empty_lines(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Check for excessive empty lines.
        """
        issues = []
        consecutive_empty = 0
        for i, line in enumerate(lines, 1):
            if not line.strip():
                consecutive_empty += 1
                if consecutive_empty > 2:
                    issues.append({
                        'line': i,
                        'type': 'empty_lines',
                        'severity': 'info',
                        'message': 'Excessive empty lines'
                    })
            else:
                consecutive_empty = 0
        return issues

    def _check_comments(self, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """
        Check for comment issues.
        """
        issues = []
        comment_pattern = self.language_patterns[language]['comment']
        comment_lines = 0
        code_lines = 0

        for i, line in enumerate(lines, 1):
            if re.search(comment_pattern, line):
                comment_lines += 1
            elif line.strip():
                code_lines += 1

        if code_lines > 0 and (comment_lines / code_lines) < 0.1:
            issues.append({
                'line': 1,
                'type': 'comments',
                'severity': 'info',
                'message': 'Low comment density'
            })

        return issues

    def _check_naming_conventions(self, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """
        Check for naming convention issues.
        """
        issues = []

        if language == 'python':
            # Check function names (should be snake_case)
            for i, line in enumerate(lines, 1):
                match = re.search(r'def\s+(\w+)\s*\(', line)
                if match:
                    func_name = match.group(1)
                    if not re.match(r'^[a-z_][a-z0-9_]*$', func_name):
                        issues.append({
                            'line': i,
                            'type': 'naming',
                            'severity': 'warning',
                            'message': f'Function name {func_name} should be snake_case'
                        })

                # Check class names (should be PascalCase)
                match = re.search(r'class\s+(\w+)\s*', line)
                if match:
                    class_name = match.group(1)
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_name):
                        issues.append({
                            'line': i,
                            'type': 'naming',
                            'severity': 'warning',
                            'message': f'Class name {class_name} should be PascalCase'
                        })

        return issues

    def _calculate_metrics(self, content: str, language: str) -> Dict[str, Any]:
        """
        Calculate code metrics.
        """
        lines = content.split('\n')
        code_lines = 0
        comment_lines = 0
        blank_lines = 0

        comment_pattern = self.language_patterns[language]['comment']

        for line in lines:
            if not line.strip():
                blank_lines += 1
            elif re.search(comment_pattern, line):
                comment_lines += 1
            else:
                code_lines += 1

        total_lines = len(lines)
        comment_ratio = (comment_lines / code_lines * 100) if code_lines > 0 else 0

        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'comment_ratio': round(comment_ratio, 2)
        }

    def _generate_recommendations(self, issues: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis results.
        """
        recommendations = []

        # Based on issues
        issue_types = set(issue['type'] for issue in issues)

        if 'indentation' in issue_types:
            recommendations.append('Fix indentation to use consistent spaces or tabs')
        if 'line_length' in issue_types:
            recommendations.append('Shorten long lines to improve readability')
        if 'empty_lines' in issue_types:
            recommendations.append('Remove excessive empty lines')
        if 'comments' in issue_types:
            recommendations.append('Add more comments to improve code clarity')
        if 'naming' in issue_types:
            recommendations.append('Follow consistent naming conventions')

        # Based on metrics
        if metrics.get('comment_ratio', 0) < 10:
            recommendations.append('Increase comment density to improve maintainability')

        if not recommendations:
            recommendations.append('Code quality looks good!')

        return recommendations


def code_review_tool(
    path: str,
    recursive: bool = False
) -> str:
    """
    Code review tool entry point.

    Args:
        path: Path to file or directory to analyze
        recursive: If True, recursively analyze directory

    Returns:
        JSON string with review results
    """
    reviewer = CodeReviewer()

    if os.path.isfile(path):
        result = reviewer.analyze_file(path)
        return json.dumps({
            'type': 'file',
            'result': result
        }, ensure_ascii=False)
    elif os.path.isdir(path):
        results = reviewer.analyze_directory(path)
        return json.dumps({
            'type': 'directory',
            'results': results
        }, ensure_ascii=False)
    else:
        return tool_error('Path not found')


def check_code_review_requirements() -> bool:
    """Code review tool has no external requirements -- always available."""
    return True


# =============================================================================
# OpenAI Function-Calling Schema
# =============================================================================

CODE_REVIEW_SCHEMA = {
    "name": "code_review",
    "description": (
        "Analyze code quality and identify potential issues. "
        "Can analyze single files or entire directories. "
        "Provides detailed analysis including issues, metrics, and recommendations."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to file or directory to analyze"
            },
            "recursive": {
                "type": "boolean",
                "description": "If True, recursively analyze directory",
                "default": False
            }
        },
        "required": ["path"]
    }
}


# --- Registry ---

registry.register(
    name="code_review",
    toolset="code",
    schema=CODE_REVIEW_SCHEMA,
    handler=lambda args, **kw: code_review_tool(
        path=args.get("path"), recursive=args.get("recursive", False)),
    check_fn=check_code_review_requirements,
    emoji="🔍",
)