"""
Unit tests for correlation_report.py module.

Tests entity correlation and relationship mapping logic.
"""

import pytest
from correlation_report import CorrelationEngine, ReportGenerator


@pytest.fixture
def engine():
    """Create CorrelationEngine instance for testing."""
    return CorrelationEngine()


@pytest.fixture
def sample_entities():
    """Sample entities for testing."""
    return {
        'source1': [
            {'value': 'admin@example.com', 'type': 'EMAIL', 'source': 'source1'},
            {'value': '192.168.1.1', 'type': 'IP_ADDRESS', 'source': 'source1'},
            {'value': 'CTF{test_flag}', 'type': 'CTF_FLAG', 'source': 'source1', 'importance_score': 1.0}
        ],
        'source2': [
            {'value': 'admin@example.com', 'type': 'EMAIL', 'source': 'source2'},
            {'value': 'johnny_ctf', 'type': 'PERSON', 'source': 'source2'}
        ]
    }


class TestCorrelationEngine:
    """Test correlation engine functionality."""
    
    def test_add_parsed_entities(self, engine, sample_entities):
        """Test adding parsed entities to correlation map."""
        engine.add_parsed_entities(sample_entities)
        
        # Check that entities are added
        assert 'admin@example.com' in engine.correlation_map
        assert '192.168.1.1' in engine.correlation_map
        assert 'ctf{test_flag}' in engine.correlation_map
    
    def test_entity_source_tracking(self, engine, sample_entities):
        """Test that entity sources are tracked correctly."""
        engine.add_parsed_entities(sample_entities)
        
        email_data = engine.correlation_map['admin@example.com']
        assert 'source1' in email_data['sources']
        assert 'source2' in email_data['sources']
        assert len(email_data['sources']) == 2
    
    def test_correlation_links_entities(self, engine, sample_entities):
        """Test that correlation finds entity links."""
        engine.add_parsed_entities(sample_entities)
        results = engine.correlate()
        
        # Email appears in both sources, should be linked
        assert results['linked_count'] > 0
    
    def test_identify_ctf_flags(self, engine, sample_entities):
        """Test identification of CTF flags."""
        engine.add_parsed_entities(sample_entities)
        results = engine.correlate()
        
        assert len(results['ctf_flags']) == 1
        assert 'ctf{test_flag}' in results['ctf_flags']
    
    def test_correlation_statistics(self, engine, sample_entities):
        """Test correlation statistics calculation."""
        engine.add_parsed_entities(sample_entities)
        results = engine.correlate()
        
        assert 'total_entities' in results
        assert 'linked_count' in results
        assert 'high_value_count' in results
        assert results['total_entities'] > 0


class TestKeyNormalization:
    """Test entity key normalization."""
    
    def test_case_insensitive_matching(self, engine):
        """Test that entity keys are case-insensitive."""
        entities1 = {
            'source1': [{'value': 'Admin@Example.COM', 'type': 'EMAIL', 'source': 'source1'}]
        }
        entities2 = {
            'source2': [{'value': 'admin@example.com', 'type': 'EMAIL', 'source': 'source2'}]
        }
        
        engine.add_parsed_entities(entities1)
        engine.add_parsed_entities(entities2)
        
        # Both should map to same normalized key
        email_data = engine.correlation_map['admin@example.com']
        assert len(email_data['sources']) == 2


class TestRelationshipDetection:
    """Test relationship detection between entities."""
    
    def test_co_occurrence_relationships(self, engine):
        """Test co-occurrence relationship detection."""
        entities = {
            'source1': [
                {'value': 'user@example.com', 'type': 'EMAIL', 'source': 'source1'},
                {'value': '192.168.1.1', 'type': 'IP_ADDRESS', 'source': 'source1'}
            ]
        }
        
        engine.add_parsed_entities(entities)
        results = engine.correlate()
        
        # Entities from same source should have relationship
        assert len(results['relationships']) > 0


class TestReportGenerator:
    """Test report generation."""
    
    def test_report_generator_initialization(self):
        """Test report generator can be initialized."""
        generator = ReportGenerator()
        assert generator is not None
        assert generator.console is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
