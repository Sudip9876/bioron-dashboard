const { DatabaseSync } = require('node:sqlite');
const fs = require('node:fs');
const path = require('node:path');

const DB_PATH = path.join(__dirname, 'bioron_operations.db');
const SCHEMA_PATH = path.join(__dirname, 'schema.sql');

// Initialize database
let dbInstance = null;

function getDb() {
    if (!dbInstance) {
        dbInstance = new DatabaseSync(DB_PATH);
        // Enable WAL mode and foreign keys
        dbInstance.exec('PRAGMA foreign_keys = ON;');
    }
    return dbInstance;
}

function initDb() {
    const db = getDb();
    if (fs.existsSync(SCHEMA_PATH)) {
        const schema = fs.readFileSync(SCHEMA_PATH, 'utf8');
        db.exec(schema);
        console.log('[DB] Database schema initialized successfully at:', DB_PATH);
    }
    return db;
}

module.exports = {
    getDb,
    initDb,
    DB_PATH
};
