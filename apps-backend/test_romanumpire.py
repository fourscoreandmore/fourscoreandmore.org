"""
Tests for Roman text validation and romanUmpire integration.

These tests ensure that:
1. Empty/template Roman text files are properly validated
2. Valid analysis files can be loaded successfully
3. Helpful error messages are provided for common issues

This prevents cryptic AttributeError from music21 9.x when parsing
files without Roman numerals.
"""

import sys
import os
import tempfile
import pytest

sys.path.insert(0, 'When-in-Rome/Code')

from romanUmpire import ScoreAndAnalysis

# Import validator directly to avoid circular imports
sys.path.insert(0, 'app')
from roman_text_validator import validate_roman_text_file


class TestRomanTextValidator:
    """Test the Roman text validation utility."""
    
    def test_empty_template_raises_error(self):
        """Empty template files (no Roman numerals) should raise ValueError."""
        template_path = "When-in-Rome/Corpus/OpenScore-LiederCorpus/Elgar,_Edward/2_Songs,_Op.60/1_The_Torch/template.txt"
        
        if not os.path.exists(template_path):
            pytest.skip(f"Template file not found: {template_path}")
        
        with pytest.raises(ValueError) as exc_info:
            validate_roman_text_file(template_path)
        
        assert "no Roman numerals" in str(exc_info.value)
        assert "template file" in str(exc_info.value)
    
    def test_valid_analysis_passes(self):
        """Valid analysis files with Roman numerals should pass validation."""
        analysis_path = "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.23/4_Auf_einem_grünen_Hügel/analysis.txt"
        
        if not os.path.exists(analysis_path):
            pytest.skip(f"Analysis file not found: {analysis_path}")
        
        # Should not raise an exception
        result = validate_roman_text_file(analysis_path)
        assert result is True
    
    def test_minimal_valid_file(self):
        """A file with minimal valid content should pass."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""Composer: Test
Title: Test
Time Signature: 4/4
m1 b1 C: I
""")
            temp_path = f.name
        
        try:
            result = validate_roman_text_file(temp_path)
            assert result is True
        finally:
            os.unlink(temp_path)
    
    def test_only_metadata_fails(self):
        """A file with only metadata and no Roman numerals should fail."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""Composer: Test
Title: Test
Analyst: Test
Time Signature: 4/4
m1 b1
m2 b1
m3 b1
""")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError) as exc_info:
                validate_roman_text_file(temp_path)
            assert "no Roman numerals" in str(exc_info.value)
        finally:
            os.unlink(temp_path)


class TestRomanUmpireIntegration:
    """Integration tests for romanUmpire with music21 9.x."""
    
    def test_load_valid_analysis(self):
        """Test that a valid analysis file loads successfully."""
        test_dir = "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.23/4_Auf_einem_grünen_Hügel"
        score_file = os.path.join(test_dir, "score.mxl")
        analysis_file = os.path.join(test_dir, "analysis.txt")
        
        if not (os.path.exists(score_file) and os.path.exists(analysis_file)):
            pytest.skip(f"Test files not found in {test_dir}")
        
        # Validate first
        validate_roman_text_file(analysis_file)
        
        # Then load with romanUmpire
        analysis = ScoreAndAnalysis(
            scoreOrData=score_file,
            analysisLocation=analysis_file
        )
        
        assert analysis is not None
        assert len(analysis.harmonicRanges) > 0
    
    def test_template_file_rejected(self):
        """Test that template files are rejected with helpful error."""
        test_dir = "When-in-Rome/Corpus/OpenScore-LiederCorpus/Elgar,_Edward/2_Songs,_Op.60/1_The_Torch"
        template_file = os.path.join(test_dir, "template.txt")
        
        if not os.path.exists(template_file):
            pytest.skip(f"Template file not found: {template_file}")
        
        with pytest.raises(ValueError) as exc_info:
            validate_roman_text_file(template_file)
        
        error_msg = str(exc_info.value)
        assert "no Roman numerals" in error_msg
        assert "template" in error_msg


if __name__ == "__main__":
    # Allow running with pytest or as a script
    pytest.main([__file__, "-v"])
