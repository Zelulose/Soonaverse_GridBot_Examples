
//note: In visual studio developer powershell install the following
//npm install sqlite3
//npm install--save - dev @types/sqlite3 ts-node typescript
import sqlite3 from 'sqlite3';

//npm install sqlite
//npm install --save-dev @types/sqlite
import { open } from 'sqlite';

//npm install rxjs
import { firstValueFrom } from 'rxjs';
import { map } from 'rxjs/operators';

//defaults from visual studio
import * as path from 'path';
import * as fs from 'fs';
import os from 'os';

//End sql headerfiles
import * as readline from 'readline';
import { Build5, https } from '@build-5/sdk';
import { Dataset } from '@build-5/interfaces';
import { otr } from '@build-5/sdk';
import { SoonaverseOtrAddress } from '@build-5/sdk';
import { SoonaverseApiKey } from '@build-5/sdk';
import { TokenTradeOrderType } from '@build-5/interfaces';

//be sure to have node.js and typescript installed ex. VS code
//npm i @build-5/sdk
//npm i @build-5/interfaces

//tsconfig.json settings for typescript
//{
//    "compilerOptions": {
//        "module": "commonjs",
//            "target": "es2017",
//                "lib": ["es2017", "dom"],
//                    "sourceMap": true,
//                        "esModuleInterop": true,
//                            "allowSyntheticDefaultImports": true
//    },
//    "exclude": [
//        "node_modules"
//    ]
//}

//You should check your file in the sdk folder for package.json for: {
//    "name": "@build-5/sdk",
//        "version": "2.2.19",
//            "description": "",
//                "main": "index.js", is in the node_modules\@build-5\sdk.the index.js isin this folder not lib\index.js
// a warning will appear in consol if you don't!

const origin = Build5.TEST

//get the soonaverse address
const otrAddress = SoonaverseOtrAddress[origin];

//Need this token from soonaverse team for the api
// soonaverse member ID to get all transactions for a token: 0x9feda995750f0884d43674da4a1859a847962760
const TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIweDU1MWZkMmM3YzdiZjM1NmJhYzE5NDU4N2RhYjJmY2Q0NjQyMDA1NGIiLCJwcm9qZWN0IjoiMHg0NjIyM2VkZDQxNTc2MzVkZmM2Mzk5MTU1NjA5ZjMwMWRlY2JmZDg4IiwiaWF0IjoxNzAwMDAyODkwfQ.IYZvBRuCiN0uYORKnVJ0SzT_1H_2o5xyDBG20VmnTQ0'; // Replace with your actual JWT token


//Note: As of April 2024 api.buildcore.io is now the API endpoint base URL is updated to the newest domain: api.buildcore.io

async function CheckTokenBuy(tokenId, LowerCaseMetaMaskID) {
    try {
        const observable = https(Build5.PROD)
            .project(SoonaverseApiKey[Build5.PROD])
            .dataset(Dataset.TOKEN_MARKET)
            .getMemberBidsLive(
                tokenId,
                LowerCaseMetaMaskID,
                TokenTradeOrderType.BUY,
            );

        // Process the data stream with RxJS operators
        const processedObservable = observable.pipe(
            
            map((o) => {
                // Format the data here as needed
                return o.map(item => ({
                    price: item.price,
                    volume: item.count,
                    state: item.status === 'active' ? 1 :
                        item.status === 'partially_settled_and_cancelled' ? 2 : 0,
                    type: 0, // Indicating sell transaction
                }));
            })
        );

        // Convert the Observable to a Promise and await the processed data
        const processedData = await firstValueFrom(processedObservable);
        return processedData;
    } catch (error) {
        console.error("Error during CheckToken:", error);
        throw error; // Rethrow or handle the error appropriately
    }
}

async function CheckTokenSell(tokenId, LowerCaseMetaMaskID) {
    try {
        const observable = https(Build5.PROD)
            .project(SoonaverseApiKey[Build5.PROD])
            .dataset(Dataset.TOKEN_MARKET)
            .getMemberBidsLive(
                tokenId,
                LowerCaseMetaMaskID,
                TokenTradeOrderType.SELL,
            );

        // Process the data stream with RxJS operators
        const processedObservable = observable.pipe(

            map((o) => {
                // Format the data here as needed
                return o.map(item => ({
                    price: item.price,
                    volume: item.count,
                    state: item.status === 'active' ? 1 :
                        item.status === 'partially_settled_and_cancelled' ? 2 : 0,
                    type: 1, // Indicating sell transaction
                }));
            })
        );

        // Convert the Observable to a Promise and await the processed data
        const processedData = await firstValueFrom(processedObservable);
        return processedData;
    } catch (error) {
        console.error("Error during CheckToken:", error);
        throw error; // Rethrow or handle the error appropriately
    }
}

//we dont use this as we will use the address and the format for metadata in python!
async function performTradeToken() {
    try {
        const otrRequestbuy = await otr(otrAddress).dataset(Dataset.TOKEN).buyToken({
            count: 10,
            symbol: 'FEE',
            price: 0.131,
            //targetAddress: 'iota1qqclp9cgd8aupzzxsftz0fqum2ha3k4kncsg2ma00se8alth3npjcxngxl7' 
            //works best with native tokens to shimmer and not iota
        });
        //console.log(otrRequestbuy) // unformated data
        // Extracting relevant fields and formatting into a new object
        const formattedOutput = {
            request: {
                count: otrRequestbuy.metadata.count,
                symbol: otrRequestbuy.metadata.symbol,
                price: otrRequestbuy.metadata.price,
                targetAddress: otrRequestbuy.metadata.targetAddress,
                requestType: otrRequestbuy.metadata.requestType
            }
        };

        // Logging the formatted output
        console.log(JSON.stringify(formattedOutput, null, 2)); //formated data
    } catch (error) {
        // Log any errors that occur during the sellBaseToken operation
        console.error(error);
    }



    // Keep the readline interface if you need to wait for user input or keep the console open
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question('Press Enter to exit...', (answer) => {
        rl.close();
    });
}
//End sample function for building metadata

type Transaction = {
    price: number;
    volume: number;
    state: number; // 1 for Active, 2 for Partially Settled and Cancelled, 0 for the rest
    type: number; // 0 for Buy, 1 for Sell
};

//these are argument inputs to help us keep our data lowercase... I am not sure what happens if the data format is wrong in length but it is probably bad (clears your databases since they dynamically update).
async function recordTransactions(tokenId: string, transactions: Transaction[]) {
    try {
        const folderPath = path.join(os.homedir(), 'Documents', 'Soonaverse Trade Data');
        // Ensure the directory exists
        await fs.promises.mkdir(folderPath, { recursive: true });

        const dbPath = path.join(folderPath, `${tokenId}.db`);

        const db = await open({
            filename: dbPath,
            driver: sqlite3.Database
        });

        await db.exec(`
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL NOT NULL,
                volume REAL NOT NULL,
                state INTEGER NOT NULL,
                type INTEGER NOT NULL
            );
        `);

        // Clear existing data
        await db.exec('DELETE FROM trades;');

        // Insert new transactions with 'type'
        const insert = 'INSERT INTO trades (price, volume, state, type) VALUES (?, ?, ?, ?);';
        for (const transaction of transactions) {
            await db.run(insert, transaction.price, transaction.volume, transaction.state, transaction.type);
        }

        console.log(`Transactions recorded for token: ${tokenId}`);

        // Close the database connection
        await db.close();
    } catch (error) {
        console.error('Error recording transactions:', error);
    }
}



function enterTokenIds(): Promise<string[]> {
    return new Promise((resolve, reject) => {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        const tokens: string[] = [];

        function askTokenId() {
            rl.question('Enter Token ID (or leave blank to finish): ', (tokenId) => {
                if (typeof tokenId === 'string') {
                    if (!tokenId.trim()) {
                        rl.close();
                        resolve(tokens.map(id => id.toLowerCase())); // Convert to lowercase
                    } else {
                        tokens.push(tokenId.trim().toLowerCase()); // Convert to lowercase
                        askTokenId();
                    }
                } else {
                    console.error('Invalid input. Please enter a string.');
                    askTokenId();
                }
            });
        }

        askTokenId();
    });
}

function enterMetamaskId(): Promise<string> {
    return new Promise((resolve, reject) => {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.question('Enter Metamask ID: ', (metamaskId) => {
            if (typeof metamaskId === 'string' && metamaskId.trim() !== '') {
                rl.close();
                resolve(metamaskId.trim().toLowerCase()); // Convert to lowercase
            } else {
                rl.close();
                reject('Invalid input. Please enter a valid Metamask ID.');
            }
        });
    });
}

const transactionsPerSecond = 1; //it takes soonaverse >15 seconds to place an order on average 
const delayBetweenTransactions = 1000 / transactionsPerSecond; // Milliseconds

(async () => {
    try {
        const metamaskIds = await enterMetamaskId();
        console.log('Metamask IDs entered:', metamaskIds);

        const tokenIds = await enterTokenIds();
        console.log('Token IDs entered:', tokenIds);
        while (true) {


            for (const tokenId of tokenIds) {
                console.log(`Processing token ID: ${tokenId}`);

                const buyTransactions = await CheckTokenBuy(tokenId, metamaskIds);
                const sellTransactions = await CheckTokenSell(tokenId, metamaskIds);

                // Optionally filter transactions based on 'state' or other criteria
                // For example, filtering active buy transactions
                const activeBuyTransactions = buyTransactions.filter(t => t.state === 1);
                const activeSellTransactions = sellTransactions.filter(t => t.state === 1);

                // Combine buy and sell transactions if needed
                const combinedTransactions = [...activeBuyTransactions, ...activeSellTransactions];

                // Record transactions to the database
                await recordTransactions(tokenId, combinedTransactions);
                console.log(`Transactions recorded successfully for token ID: ${tokenId}`);
                console.log(combinedTransactions);
                await sleep(delayBetweenTransactions); // Wait before processing next token ID
            }
        }
    } catch (error) {
        console.error("An error occurred:", error);
    }
})();

function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


//performTradeToken();


//Note: 
//
//    unlimited number of requests on OTR through Tangle - recommended!
//    maximum of 50 requests per second on GET requests
//    maximum of 5 requests per second on POST requests

