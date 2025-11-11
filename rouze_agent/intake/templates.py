# ~/Desktop/rouze/rouze_agent/intake/templates.py

class IntakeTemplate:
    """Dynamic client intake questionnaire system"""
    
    INDUSTRY_TEMPLATES = {
        'healthcare': {
            'initial_questions': [
                {
                    'id': 'hc_001',
                    'question': 'What specific decision are you trying to make?',
                    'type': 'textarea',
                    'required': True,
                    'placeholder': 'e.g., Should we launch product X in market Y?'
                },
                {
                    'id': 'hc_002',
                    'question': 'What is your product/service category?',
                    'type': 'select',
                    'options': ['Pharmaceutical', 'Medical Device', 'Digital Health', 'Provider Services', 'Other'],
                    'required': True
                },
                {
                    'id': 'hc_003',
                    'question': 'What data sources do you currently use?',
                    'type': 'multiselect',
                    'options': ['Clinical trials', 'Patient forums', 'FDA databases', 'Physician surveys', 'None'],
                    'required': False
                },
                {
                    'id': 'hc_004',
                    'question': 'What is your timeline for this decision?',
                    'type': 'select',
                    'options': ['Urgent (< 48 hours)', 'High priority (3-7 days)', 'Standard (7-14 days)', 'Flexible (> 14 days)'],
                    'required': True
                },
                {
                    'id': 'hc_005',
                    'question': 'What competitors should we analyze?',
                    'type': 'textarea',
                    'required': False,
                    'placeholder': 'List 3-5 main competitors or "unsure"'
                }
            ],
            'follow_up_logic': {
                # Conditional follow-up questions based on answers
                'hc_002': {
                    'Pharmaceutical': [
                        {
                            'id': 'hc_pharma_001',
                            'question': 'What therapeutic area?',
                            'type': 'text',
                            'required': True
                        },
                        {
                            'id': 'hc_pharma_002',
                            'question': 'Are you tracking adverse events or efficacy signals?',
                            'type': 'radio',
                            'options': ['Adverse events', 'Efficacy', 'Both', 'Neither'],
                            'required': True
                        }
                    ],
                    'Medical Device': [
                        {
                            'id': 'hc_device_001',
                            'question': 'Device classification (Class I, II, or III)?',
                            'type': 'select',
                            'options': ['Class I', 'Class II', 'Class III', 'Unsure'],
                            'required': False
                        }
                    ]
                }
            }
        },
        
        'saas': {
            'initial_questions': [
                {
                    'id': 'saas_001',
                    'question': 'What specific decision are you trying to make?',
                    'type': 'textarea',
                    'required': True
                },
                {
                    'id': 'saas_002',
                    'question': 'What is your product category?',
                    'type': 'select',
                    'options': ['Project Management', 'CRM', 'Marketing Automation', 'Developer Tools', 'Other'],
                    'required': True
                },
                {
                    'id': 'saas_003',
                    'question': 'What feature gaps are you investigating?',
                    'type': 'textarea',
                    'required': False,
                    'placeholder': 'What features do you think customers want?'
                },
                {
                    'id': 'saas_004',
                    'question': 'Target market size',
                    'type': 'select',
                    'options': ['SMB (< 50 employees)', 'Mid-market (50-500)', 'Enterprise (> 500)', 'All segments'],
                    'required': True
                }
            ],
            'follow_up_logic': {
                'saas_002': {
                    'Project Management': [
                        {
                            'id': 'saas_pm_001',
                            'question': 'Which competitors should we analyze?',
                            'type': 'multiselect',
                            'options': ['Asana', 'Monday.com', 'ClickUp', 'Jira', 'Other'],
                            'required': True
                        }
                    ]
                }
            }
        },
        
        'ecommerce': {
            'initial_questions': [
                {
                    'id': 'ec_001',
                    'question': 'What specific decision are you trying to make?',
                    'type': 'textarea',
                    'required': True
                },
                {
                    'id': 'ec_002',
                    'question': 'What product category are you selling?',
                    'type': 'text',
                    'required': True,
                    'placeholder': 'e.g., sustainable home goods'
                },
                {
                    'id': 'ec_003',
                    'question': 'Primary sales channel',
                    'type': 'multiselect',
                    'options': ['Amazon', 'Shopify store', 'TikTok Shop', 'Instagram', 'Other marketplace'],
                    'required': True
                },
                {
                    'id': 'ec_004',
                    'question': 'What intelligence do you need?',
                    'type': 'radio',
                    'options': ['Trend prediction', 'Competitor analysis', 'Customer sentiment', 'All of above'],
                    'required': True
                }
            ]
        }
    }
    
    @classmethod
    def get_template(cls, industry):
        """Retrieve intake template for specific industry"""
        return cls.INDUSTRY_TEMPLATES.get(industry.lower(), cls.INDUSTRY_TEMPLATES['saas'])
    
    @classmethod
    def generate_follow_ups(cls, industry, initial_answers):
        """Generate adaptive follow-up questions based on initial answers"""
        template = cls.get_template(industry)
        follow_up_questions = []
        
        for question_id, answer in initial_answers.items():
            if question_id in template.get('follow_up_logic', {}):
                # Check if answer triggers follow-up questions
                if answer in template['follow_up_logic'][question_id]:
                    follow_up_questions.extend(
                        template['follow_up_logic'][question_id][answer]
                    )
        
        return follow_up_questions