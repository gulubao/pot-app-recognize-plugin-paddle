async function recognize(base64, lang, options) {
    const { utils } = options;
    const { run, cacheDir, pluginDir, osType } = utils;

    // Service configuration
    const SERVICE_PORT = 28123;
    const SERVICE_HOST = '127.0.0.1';
    const SERVICE_URL = `http://${SERVICE_HOST}:${SERVICE_PORT}`;
    const STARTUP_TIMEOUT = 15000; // 15 seconds
    const REQUEST_TIMEOUT = 30000;  // 30 seconds

    try {
        // Start OCR service if not running
        await ensureServiceRunning(SERVICE_URL, pluginDir, osType, run);
        
        // Make OCR request
        const response = await fetch(`${SERVICE_URL}/ocr`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: base64,
                language: lang
            }),
            signal: AbortSignal.timeout(REQUEST_TIMEOUT)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`OCR service error: ${response.status} - ${errorData.error || 'Unknown error'}`);
        }

        const result = await response.json();
        
        if (result.status !== 'success') {
            throw new Error(result.error || 'OCR processing failed');
        }

        // Extract text from results (compatible with old format)
        let text = '';
        if (result.data && Array.isArray(result.data)) {
            for (const item of result.data) {
                if (item.text) {
                    text += `${item.text}
`;
                }
            }
        }

        return text.trim();

    } catch (error) {
        throw new Error(`PaddleOCR recognition failed: ${error.message}`);
    }
}

async function ensureServiceRunning(serviceUrl, pluginDir, osType, runCommand) {
    // Check if service is already running
    try {
        const response = await fetch(`${serviceUrl}/health`, {
            signal: AbortSignal.timeout(2000)
        });
        if (response.ok) {
            return; // Service is running
        }
    } catch (error) {
        // Service not running, need to start it
    }

    // Start the service
    const pythonCmd = getPythonCommand(osType);
    const servicePath = `${pluginDir}/ocr_service.py`;
    
    try {
        // Start service in background
        const serviceProcess = runCommand(pythonCmd, [servicePath], {
            detached: true,
            stdio: 'ignore'
        });

        // Wait for service to be ready
        const startTime = Date.now();
        while (Date.now() - startTime < 15000) { // 15 second timeout
            try {
                const response = await fetch(`${serviceUrl}/health`, {
                    signal: AbortSignal.timeout(1000)
                });
                if (response.ok) {
                    return; // Service is ready
                }
            } catch (error) {
                // Still starting, wait a bit more
            }
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        throw new Error('Service startup timeout');
        
    } catch (error) {
        throw new Error(`Failed to start OCR service: ${error.message}`);
    }
}

function getPythonCommand(osType) {
    // Determine appropriate Python command based on OS
    switch (osType) {
        case 'windows':
            return 'python';
        case 'macos':
        case 'linux':
        default:
            return 'python3';
    }
} = options;
    const { run, cacheDir, pluginDir } = utils;

    let result = await run(`${pluginDir}/PaddleOCR-json.exe`, [
        "use_angle_cls=true",
        "cls=true",
        `--image_path=${cacheDir}/pot_screenshot_cut.png`,
        `--config_path=models/config_${lang}.txt`,
    ]);
    if (result.status === 0) {
        let out = result.stdout;
        out = out.split("OCR init completed.");
        out = out[1].trim();
        let json = JSON.parse(out);
        let target = "";
        for (let line of json.data) {
            target += `${line.text}\n`;
        }
        return target.trim();
    } else {
        throw Error(result.stderr);
    }
}