<?php
// Database credentials
$host = '127.0.0.1';
$dbname = 'college_assets_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Get all tables from the database
    $stmt = $pdo->prepare("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :dbname AND TABLE_TYPE = 'BASE TABLE'");
    $stmt->execute(['dbname' => $dbname]);
    $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
    
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Database Dictionary - <?php echo htmlspecialchars($dbname); ?></title>
<style>
    :root {
        --pink-50: #fdf2f8;
        --pink-100: #fce7f3;
        --pink-200: #fbcfe8;
        --pink-600: #db2777;
        --pink-800: #9d174d;
        --pink-900: #831843;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: var(--pink-50);
        color: #333;
        margin: 0;
        padding: 40px 20px;
    }
    
    .dictionary-container {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .main-title {
        color: var(--pink-900);
        text-align: center;
        margin-bottom: 40px;
        font-size: 2.5em;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .table-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(219, 39, 119, 0.1);
        margin-bottom: 50px;
        overflow: hidden;
        border: 1px solid var(--pink-200);
    }
    
    .table-header {
        background-color: var(--pink-600);
        color: white;
        padding: 15px 25px;
        font-size: 1.5em;
        font-weight: bold;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
    }
    
    th, td {
        padding: 15px 25px;
        text-align: left;
        border-bottom: 1px solid var(--pink-100);
    }
    
    th {
        background-color: var(--pink-100);
        color: var(--pink-900);
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9em;
        letter-spacing: 1px;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    tr:hover {
        background-color: var(--pink-50);
    }
    
    .type-badge {
        display: inline-block;
        background-color: var(--pink-100);
        color: var(--pink-800);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85em;
        font-family: monospace;
    }
    
    .constraint-item {
        display: inline-block;
        background-color: #f3f4f6;
        color: #4b5563;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin: 2px;
    }
    
    .constraint-pk { background-color: #fef08a; color: #854d0e; }
    .constraint-fk { background-color: #bfdbfe; color: #1e3a8a; }
    .constraint-nn { background-color: #fecaca; color: #991b1b; }

    /* Print friendly styles */
    @media print {
        body {
            background-color: white;
            padding: 0;
        }
        .dictionary-container {
            max-width: 100%;
        }
        .table-container {
            box-shadow: none;
            border: 1px solid #ccc;
            page-break-inside: avoid;
            page-break-after: always;
            margin-bottom: 20px;
        }
        .table-container:last-child {
            page-break-after: auto;
        }
        .table-header {
            background-color: #eee !important;
            color: #000 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        th {
            background-color: #f9f9f9 !important;
            color: #000 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        .type-badge, .constraint-item {
            border: 1px solid #ccc;
            background: transparent !important;
        }
    }
</style>
</head>
<body>
    <div class="dictionary-container">
        <h1 class="main-title">Database Dictionary</h1>
        
        <?php foreach ($tables as $table): ?>
            <div class="table-container">
                <div class="table-header">
                    Table: <?php echo htmlspecialchars($table); ?>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th width="20%">Field</th>
                            <th width="20%">Type</th>
                            <th width="30%">Constraints</th>
                            <th width="30%">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $colStmt = $pdo->prepare("
                            SELECT 
                                COLUMN_NAME, 
                                COLUMN_TYPE, 
                                IS_NULLABLE, 
                                COLUMN_KEY, 
                                COLUMN_DEFAULT, 
                                EXTRA, 
                                COLUMN_COMMENT
                            FROM INFORMATION_SCHEMA.COLUMNS 
                            WHERE TABLE_SCHEMA = :dbname AND TABLE_NAME = :tablename
                            ORDER BY ORDINAL_POSITION
                        ");
                        $colStmt->execute(['dbname' => $dbname, 'tablename' => $table]);
                        $columns = $colStmt->fetchAll(PDO::FETCH_ASSOC);
                        
                        foreach ($columns as $col):
                            $constraints = [];
                            if ($col['COLUMN_KEY'] == 'PRI') $constraints[] = '<span class="constraint-item constraint-pk">PRIMARY KEY</span>';
                            if ($col['COLUMN_KEY'] == 'UNI') $constraints[] = '<span class="constraint-item constraint-fk">UNIQUE</span>';
                            if ($col['COLUMN_KEY'] == 'MUL') $constraints[] = '<span class="constraint-item constraint-fk">INDEX/FK</span>';
                            if ($col['IS_NULLABLE'] == 'NO') $constraints[] = '<span class="constraint-item constraint-nn">NOT NULL</span>';
                            if ($col['EXTRA']) $constraints[] = '<span class="constraint-item">' . htmlspecialchars(strtoupper($col['EXTRA'])) . '</span>';
                            if ($col['COLUMN_DEFAULT'] !== null) $constraints[] = '<span class="constraint-item">DEFAULT: ' . htmlspecialchars($col['COLUMN_DEFAULT']) . '</span>';
                        ?>
                        <tr>
                            <td><strong><?php echo htmlspecialchars($col['COLUMN_NAME']); ?></strong></td>
                            <td><span class="type-badge"><?php echo htmlspecialchars($col['COLUMN_TYPE']); ?></span></td>
                            <td><?php echo implode(' ', $constraints); ?></td>
                            <td><?php echo htmlspecialchars($col['COLUMN_COMMENT'] ? $col['COLUMN_COMMENT'] : '—'); ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endforeach; ?>
        
        <?php if(empty($tables)): ?>
            <div class="table-container" style="padding: 30px; text-align: center;">
                <p>No tables found in the database <strong><?php echo htmlspecialchars($dbname); ?></strong>.</p>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
