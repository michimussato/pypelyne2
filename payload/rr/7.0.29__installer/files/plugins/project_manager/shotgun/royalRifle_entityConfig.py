""" this module holds all information needed for the entity
	

	To add tracked fields,to the different entity types please use the following schema::
	
		[
			...
			{
				'type' : 'FIELD_TYPE_NAME',
				'name' : 'FIELD_NAME',
				'input' : {'OPTION': OPTION_VALUE}
			},
			...
		]
	
	there are 5 entities, which can be changed by this config::
	
		#1) jobEntityType
		#2) submitEntityType
		#3) Shot
		#4) Sequence
		#5) Task
	
"""

import rrSG

submitEntityFields = [
		{'type' : 'entity',
			'name' : 'linked_sequence',
			'input' : {'valid_types':['Sequence']}
		},
		{'type' : 'entity',
			'name' : 'linked_shot',
			'input' : {'valid_types':['Shot']}
		},
		{'type' : 'entity',
			'name' : 'linked_task',
			'input' : {'valid_types':['Task']}
		},
		{'type' : 'entity',
			'name' : 'linked_user',
			'input' : {'valid_types':['HumanUser']}
		},
		{'type' : 'multi_entity',
			'name' : 'linked_jobs',
			'input' : {'valid_types':[rrSG.entityJob()]}
		},
		{'type' : 'text',
			'name' : 'render_application',
		},
		{'type' : 'url',
			'name' : 'render_scene_name',
			'input' : {'open_in_new_window': True},
		},
	]


jobEntityFields = [
		{'type' : 'entity',
			'name' : 'linked_submit_entity',
			'input' : {'valid_types':[rrSG.entitySubmit()]}
		},
		{'type' : 'text',
			'name' : 'render_pass',
		},
		{'type' : 'text',
			'name' : 'render_camera',
		},
		{'type' : 'text',
			'name' : 'average_render_time',
		},
		{'type' : 'float',
			'name' : 'average_memory_usage',
		},
		{'type' : 'number',
			'name' : 'frames',
		},
		{'type' : 'text',
			'name' : 'job_id',
		},
	]

shotFields =  [
		{'type' : 'multi_entity',
			'name' : 'royal_render_watch',
			'input' : {'valid_types':[rrSG.entitySubmit()]}
		},
	]

sequenceFields = [
		{'type' : 'multi_entity',
			'name' : 'royal_render_watch',
			'input' : {'valid_types':[rrSG.entitySubmit()]}
		},
	]

taskFields = [
		{'type' : 'multi_entity',
			'name' : 'royal_render_watch',
			'input' : {'valid_types':[rrSG.entitySubmit()]}
		},
	]
