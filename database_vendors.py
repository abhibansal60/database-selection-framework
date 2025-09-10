#!/usr/bin/env python3
"""
Database Vendor Configuration System

Defines supported databases and their characteristics for the selection framework.
Easily extensible to add new database vendors.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum

class DatabaseCategory(Enum):
    RELATIONAL = "relational"
    DOCUMENT = "document" 
    KEY_VALUE = "key_value"
    GRAPH = "graph"
    COLUMNAR = "columnar"
    MULTI_MODEL = "multi_model"

@dataclass
class DatabaseVendor:
    """Configuration for a database vendor"""
    id: str
    name: str
    category: DatabaseCategory
    description: str
    strengths: List[str]
    considerations: List[str]
    ideal_for: List[str]
    learning_curve: str  # "Low", "Medium", "High"
    ecosystem_maturity: str  # "Emerging", "Mature", "Enterprise"
    scaling_model: str  # "Vertical", "Horizontal", "Both"

class DatabaseRegistry:
    """Registry of supported database vendors"""
    
    def __init__(self):
        self.vendors = {}
        self._initialize_vendors()
    
    def _initialize_vendors(self):
        """Initialize default database vendors"""
        
        # PostgreSQL
        self.vendors['postgresql'] = DatabaseVendor(
            id='postgresql',
            name='PostgreSQL',
            category=DatabaseCategory.RELATIONAL,
            description='Advanced open-source relational database with JSON support',
            strengths=[
                'ACID compliance and strong consistency',
                'Advanced SQL features and complex queries',
                'JSON/JSONB support for flexibility',
                'Mature ecosystem and tooling',
                'Excellent performance for complex queries',
                'Strong community support'
            ],
            considerations=[
                'Schema migrations can be complex',
                'Vertical scaling limitations',
                'Learning curve for advanced features',
                'Memory usage can be high'
            ],
            ideal_for=[
                'Applications with complex relational data',
                'Financial systems requiring ACID properties',
                'Analytics and reporting workloads',
                'Teams with SQL expertise',
                'Applications needing both relational and document features'
            ],
            learning_curve='Medium',
            ecosystem_maturity='Enterprise',
            scaling_model='Vertical'
        )
        
        # MongoDB
        self.vendors['mongodb'] = DatabaseVendor(
            id='mongodb',
            name='MongoDB',
            category=DatabaseCategory.DOCUMENT,
            description='Document-oriented NoSQL database with horizontal scaling',
            strengths=[
                'Schema flexibility and evolution',
                'JSON-native document model',
                'Horizontal scaling capabilities',
                'Rapid prototyping and development',
                'Rich query language for documents',
                'Strong developer experience'
            ],
            considerations=[
                'Limited join support',
                'Eventual consistency model',
                'Memory usage for working set',
                'Schema design requires planning'
            ],
            ideal_for=[
                'Rapid prototyping and agile development',
                'Content management systems',
                'Catalogs and inventory systems',
                'IoT and sensor data collection',
                'Applications with evolving schemas'
            ],
            learning_curve='Low',
            ecosystem_maturity='Mature',
            scaling_model='Horizontal'
        )
        
        # MySQL
        self.vendors['mysql'] = DatabaseVendor(
            id='mysql',
            name='MySQL',
            category=DatabaseCategory.RELATIONAL,
            description='Popular open-source relational database',
            strengths=[
                'Wide adoption and community',
                'Excellent performance for read workloads',
                'Simple setup and administration',
                'Cost-effective scaling options',
                'Rich ecosystem of tools',
                'JSON support in recent versions'
            ],
            considerations=[
                'Limited advanced SQL features compared to PostgreSQL',
                'Storage engine complexity',
                'Replication can be complex',
                'Less sophisticated JSON handling'
            ],
            ideal_for=[
                'Web applications and CMS',
                'E-commerce platforms',
                'Content-driven applications',
                'Teams familiar with traditional SQL',
                'Cost-sensitive projects'
            ],
            learning_curve='Low',
            ecosystem_maturity='Enterprise',
            scaling_model='Both'
        )
        
        # Redis
        self.vendors['redis'] = DatabaseVendor(
            id='redis',
            name='Redis',
            category=DatabaseCategory.KEY_VALUE,
            description='In-memory data structure store with persistence options',
            strengths=[
                'Extremely fast in-memory operations',
                'Rich data types (sets, lists, hashes)',
                'Pub/sub messaging capabilities',
                'Simple key-value operations',
                'Excellent for caching and sessions',
                'Atomic operations'
            ],
            considerations=[
                'Memory-based storage limits dataset size',
                'Persistence configuration critical',
                'Single-threaded for commands',
                'Not suitable as primary database for most apps'
            ],
            ideal_for=[
                'Caching layers',
                'Session storage',
                'Real-time analytics',
                'Message queuing',
                'Leaderboards and counters'
            ],
            learning_curve='Low',
            ecosystem_maturity='Mature',
            scaling_model='Horizontal'
        )
        
        # Elasticsearch
        self.vendors['elasticsearch'] = DatabaseVendor(
            id='elasticsearch',
            name='Elasticsearch',
            category=DatabaseCategory.DOCUMENT,
            description='Distributed search and analytics engine',
            strengths=[
                'Full-text search capabilities',
                'Real-time analytics and aggregations',
                'Horizontal scaling and sharding',
                'RESTful API interface',
                'Rich query DSL',
                'Near real-time indexing'
            ],
            considerations=[
                'Complex cluster management',
                'Resource intensive',
                'Not ACID compliant',
                'Steep learning curve for optimization'
            ],
            ideal_for=[
                'Search-heavy applications',
                'Log and event analysis',
                'Business intelligence dashboards',
                'Content discovery systems',
                'Monitoring and observability'
            ],
            learning_curve='High',
            ecosystem_maturity='Mature',
            scaling_model='Horizontal'
        )
    
    def get_vendor(self, vendor_id: str) -> DatabaseVendor:
        """Get vendor by ID"""
        return self.vendors.get(vendor_id)
    
    def get_all_vendors(self) -> Dict[str, DatabaseVendor]:
        """Get all registered vendors"""
        return self.vendors
    
    def get_vendors_by_category(self, category: DatabaseCategory) -> Dict[str, DatabaseVendor]:
        """Get vendors filtered by category"""
        return {k: v for k, v in self.vendors.items() if v.category == category}
    
    def add_vendor(self, vendor: DatabaseVendor):
        """Add a custom vendor to the registry"""
        self.vendors[vendor.id] = vendor
    
    def get_vendor_comparison_pairs(self) -> List[List[str]]:
        """Get common vendor comparison pairs"""
        return [
            ['postgresql', 'mongodb'],  # Classic SQL vs NoSQL
            ['postgresql', 'mysql'],    # PostgreSQL vs MySQL
            ['mongodb', 'elasticsearch'], # Document stores
            ['redis', 'postgresql'],    # Cache vs primary DB
            ['mysql', 'mongodb'],       # Traditional vs modern
        ]

# Global registry instance
database_registry = DatabaseRegistry()