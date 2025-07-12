# Product Requirements Document: Integrating Asma al-Husna CLI with Notion "The Draw" Database

## Executive Summary

This document outlines the integration requirements for connecting the `asma_al_husna_cli` application with the Notion workspace's "The Draw" database system. The integration will automate the daily divine name selection process for both Ayshe and Kai, updating their respective Notion journal entries with the selected names and maintaining the spiritual practice workflow.

## Current System Analysis

### Notion Workspace Structure

#### The Draw Page
- **Location**: Root workspace page
- **Purpose**: Central hub for daily spiritual practice tracking
- **Structure**: Contains two columns with separate databases for Ayshe and Kai

#### Database Architecture

1. **Ayshe's Cards Database** (`224633e8-8fdf-800f-acec-ec9c17cab939`)
   - **Properties**:
     - `Journal` (title): Journal entry title
     - `Day` (created_time): Timestamp of creation
     - `Date` (date): Optional date field
     - `Prompt` (rich_text): User's intention/prayer
     - `Person` (people): Linked to Ayshe's user
     - `Al-Asma al-Husna` (relation): Links to the main names database
     - `ID` (unique_id): Auto-generated unique identifier

2. **Kai's Cards Database** (`224633e8-8fdf-8035-a9ca-ecb77fcef56d`)
   - **Properties**: Similar structure to Ayshe's database
   - **Person**: Linked to Kai's user

3. **Al-Asma al-Husna Database** (`224633e8-8fdf-8058-96e8-d6c599072772`)
   - **Properties**:
     - `The Beautiful Name` (title): Name in Arabic and transliteration
     - `Number`: Traditional numbering (1-99)
     - `Brief Meaning`: English translation
     - `Ta'wil`: Four levels of interpretation
     - `Quranic Reference`: Relevant verses
     - `Dhikr Formula`: Meditation practices
     - `Ayshe Drew` & `Kai Drew` (relations): Backlinks to their respective databases

### Daily Workflow

1. **0430hrs**: New rows are automatically created in both Ayshe's and Kai's databases
2. **Post-0430hrs**: CLI should run to:
   - Select a divine name for Ayshe
   - Select a divine name for Kai
   - Update their respective database entries
   - Link to the appropriate name in the Al-Asma al-Husna database

### Template Structure

Each daily entry includes a journaling template with sections for:
- Four Levels of Understanding (Sharī'a, Ṭarīqa, Ḥaqīqa, Ma'rifa)
- Evening Reflection prompts
- Personal insights and learnings

## Integration Requirements

### Functional Requirements

#### FR1: CLI Command Enhancement
- Modify the `meditate` command to support multiple user draws
- Add new command: `meditate --notion-sync` or similar
- Support for specifying users: `--users ayshe,kai`

#### FR2: Notion API Integration
- Authenticate with Notion API using the existing MCP connection
- Query the most recent (today's) entries in both databases
- Update entries with selected divine names
- Create proper relations to the Al-Asma al-Husna database

#### FR3: User Intention Handling
- Option to pre-define intentions for each user
- Support for reading intentions from configuration file
- Fallback to default intentions if not provided

#### FR4: Name Selection Logic
- Ensure both users receive different names on the same day
- Maintain the ultra-random selection algorithm
- Track previously selected names to avoid recent repetitions

### Technical Requirements

#### TR1: Configuration Management
- Store Notion database IDs in configuration
- User mapping (Ayshe/Kai to their Notion user IDs)
- API credentials management (leverage existing MCP setup)

#### TR2: Error Handling
- Graceful handling of Notion API failures
- Retry logic for transient errors
- Clear error messages for configuration issues

#### TR3: Logging and Monitoring
- Log successful updates with timestamp
- Track which names were assigned to which users
- Optional verbose mode for debugging

### Integration Architecture

```
┌─────────────────────┐
│   CLI Application   │
│  (main.py)          │
└──────────┬──────────┘
           │
    ┌──────▼──────────┐
    │ Notion Service  │
    │   Module         │
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │   MCP Notion    │
    │   Integration   │
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │  Notion API     │
    │  Workspace      │
    └─────────────────┘
```

## Implementation Plan

### Phase 1: Core Integration Module
1. Create `notion_integration.py` module
2. Implement Notion API wrapper using MCP tools
3. Add configuration management for database IDs

### Phase 2: CLI Enhancement
1. Extend `meditate` command with Notion sync options
2. Implement multi-user draw logic
3. Add intention management

### Phase 3: Database Operations
1. Implement query for today's entries
2. Create update functions for journal entries
3. Handle relation creation to Al-Asma database

### Phase 4: Testing & Refinement
1. Test with sample data
2. Implement error handling
3. Add logging and monitoring

## Configuration Schema

```python
# config.yaml or .env structure
notion:
  databases:
    ayshe_cards: "224633e8-8fdf-800f-acec-ec9c17cab939"
    kai_cards: "224633e8-8fdf-8035-a9ca-ecb77fcef56d"
    asma_al_husna: "224633e8-8fdf-8058-96e8-d6c599072772"
  
  users:
    ayshe:
      notion_id: "219d872b-594c-81d2-a706-0002658170f0"
      default_intention: "I seek divine guidance"
    kai:
      notion_id: "212d872b-594c-8181-aae4-0002a68ed0ae"
      default_intention: "Show me the path"
```

## API Integration Points

### 1. Query Today's Entries
```python
# Find entries created today at 0430hrs
filter = {
    "property": "Day",
    "created_time": {
        "on_or_after": today_0430
    }
}
```

### 2. Update Journal Entry
```python
# Update with selected name and relation
properties = {
    "Al-Asma al-Husna": {
        "relation": [{"id": selected_name_id}]
    },
    "Prompt": {
        "rich_text": [{"text": {"content": intention}}]
    }
}
```

### 3. Title Generation
```python
# Generate title: "Journey with The Name: [Name]"
title = f"Journey with The Name: {selected_name.name_arabic} ({selected_name.transliteration})"
```

## Success Criteria

1. **Automation**: CLI successfully updates both users' daily entries
2. **Accuracy**: Correct names are linked with proper relations
3. **Reliability**: Consistent operation every day after 0430hrs
4. **Usability**: Clear feedback on successful updates
5. **Maintainability**: Well-documented code with error handling

## Future Enhancements

1. **Scheduling**: Built-in scheduler to run automatically at specified time
2. **Analytics**: Track name distribution and patterns over time
3. **Notifications**: Send notifications when daily draw is complete
4. **Web Interface**: Optional web UI for manual draws
5. **Multi-language**: Support for additional languages in journal entries

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|---------|------------|
| Notion API changes | High | Version lock API, monitor deprecations |
| Rate limiting | Medium | Implement exponential backoff |
| Duplicate draws | Low | Add deduplication logic |
| Time zone issues | Medium | Use UTC internally, convert for display |

## Conclusion

This integration will streamline the daily spiritual practice workflow by automating the divine name selection and Notion database updates. The solution maintains the sacred nature of the practice while reducing manual overhead and ensuring consistency in the daily routine.