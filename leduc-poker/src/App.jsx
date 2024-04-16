import { useState, useEffect } from 'react';
import './App.css';
import botState from '../../server/state.json';

//for the images
import JC from './assets/cards/JC.jpg';
import KC from './assets/cards/KC.jpg';
import QC from './assets/cards/QC.jpg';
import JD from './assets/cards/JD.jpg';
import KD from './assets/cards/KD.jpg';
import QD from './assets/cards/QD.jpg';
import JH from './assets/cards/JH.jpg';
import KH from './assets/cards/KH.jpg';
import QH from './assets/cards/QH.jpg';
import JS from './assets/cards/JS.jpg';
import KS from './assets/cards/KS.jpg';
import QS from './assets/cards/QS.jpg';
import Back from './assets/cards/back.jpg';

function LeducHoldem() {
  const deck = ['J', 'Q', 'K'];
  const suits = ['C', 'D']; // Optional for visual representation
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [roundNum, setRoundNum] = useState(0);

  const [gameState, setGameState] = useState({
    pot: botState.pot,
    playerCard: null,
    botCard: null,
    communityCard: null,
    isBettingRound: true,
    gameOver: false,
    secondRound: false,
    highlightBtn: null
  });

  const handleBet = () => {
    const action = "raise";
    try {
      const response = fetch('http://localhost:5000/action', {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
        body: JSON.stringify({ action }), // Send updated value in JSON
      });
  
      if (response.ok) {
        setGameState({
          ...gameState,
          gameOver: true,
          highlightBtn: botState.suggested_action
        });
        console.log('Value updated successfully!');
      } else {
        console.error('Error updating value:', response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
    getResult();
  }; 

  const handleCheck = () => {
    const action = "call";
    try {
      const response = fetch('http://localhost:5000/action', {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
        body: JSON.stringify({ action }), // Send updated value in JSON
      });
  
      if (response.ok) {
        setGameState({
          ...gameState,
          gameOver: true,
          highlightBtn: botState.suggested_action
        });
        console.log('Value updated successfully!');
      } else {
        console.error('Error updating value:', response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  const handleFold = async () => {
    const action = "fold";
    try {
      const response = await fetch('http://localhost:5000/action', {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
        body: JSON.stringify({ action }), // Send updated value in JSON
      });
  
      if (response.ok) {
        setGameState({
          ...gameState,
          gameOver: true,
          highlightBtn: botState.suggested_action
        });
        console.log('Value updated successfully!');
      } else {
        console.error('Error updating value:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const getResult = async () => {
    try {
      if (botState.result != null){
        setGameState({
          ...gameState,
          gameOver: true
        })
      }
    } catch (error) {
      if (botState.result != null){
      setGameState({
        ...gameState,
        gameOver: true
      })
    }
    }
  };

  const determineWinner = () => {
    if (botState.result == "win"){
      return "You win!";
    }

    if (botState.result == "loss"){
      return "You lose :("
    }

    if (botState.result == "draw"){
      return "Draw!"
    }
  };

  const handleNextRound = async () => {
    console.log('handleNextRound')
    const action = true;
    try {
      const response = await fetch('http://localhost:5000/update/new_round', {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
        body: JSON.stringify({ action }), // Send updated value in JSON
      });
  
      if (response.ok) {
        setGameState({
          ...gameState,
          gameOver: false
        });
        console.log(gameState.gameOver)
        console.log('Value updated successfully!');
      } else {
        console.error('Error updating value:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    setGameState({
      ...gameState,
      gameOver: false
    });
  }, [gameState.gameOver]);

  //for the images
  const cardOut = (cardOwner) => {
    let suit = null;
    let cardVal = null

    if (cardOwner == 'Player'){
      suit = botState.player_hand[0];
      cardVal = botState.player_hand[1];
    }

    if (cardOwner == 'Public'){
      try{
        suit = botState.public_card[0];
        cardVal = botState.public_card[1];
      }
      catch {
        return Back;
      }
    }

    if (cardOwner == 'Bot'){
      try {
        suit = botState.bot_card[0];
        cardVal = botState.bot_card[1];
        getResult();
      } 
      catch{
        return Back;
      }
    }

    if (suit == 'C'){
      if (cardVal == 'J'){
        return JC;
      }
      if (cardVal == 'Q'){
        return QC;
      }
      if (cardVal == 'K'){
        return KC;
      }
    }

    if (suit == 'D'){
      if (cardVal == 'J'){
        return JD;
      }
      if (cardVal == 'Q'){
        return QD;
      }
      if (cardVal == 'K'){
        return KD;
      }
    }

    if (suit == 'H'){
      if (cardVal == 'J'){
        return JH;
      }
      if (cardVal == 'Q'){
        return QH;
      }
      if (cardVal == 'K'){
        return KH;
      }
    }

    if (suit == 'S'){
      if (cardVal == 'J'){
        return JS;
      }
      if (cardVal == 'Q'){
        return QS;
      }
      if (cardVal == 'K'){
        return KS;
      }
    }
    else{
      return Back;
    }
  };

  const getData = async () => {
    if (botState.result != null){
      setGameState({
        ...gameState,
        gameOver: true
      });
    }
    else{
      setGameState({
        ...gameState,
        gameOver: false
      });
    }

    setGameState({
      ...gameState,
      pot: botState.pot,
      playerCard: cardOut(botState.state.hand),
      communityCard: cardOut(botState.state.public_card),
      botCard: Back //for now
    });

    console.log(botState.state);
  };

  const {gameOver, isBettingRound, playerCard} = gameState

  //this shows the cards in the ui
  const showCards = () => {
    return(
      <div>
        <div style={{
          backgroundColor: '#2f3136',
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: "translate(-50%, -50%)",
          paddingLeft: '15px',
          paddingRight: '15px',
          paddingBottom: '5px',
          borderRadius: '10px'
        }}>
          <h2> Community Card: </h2>
          <img src={cardOut("Public")}/> 
        </div>

        <div style={{
          backgroundColor: '#2f3136',
          position: 'absolute',
          left: '30%',
          top: '50%',
          msTransform: "translateY(-50%)",
          transform: "translateY(-50%)",
          paddingLeft: '15px',
          paddingRight: '15px',
          paddingBottom: '5px',
          borderRadius: '10px'
        }}>
          <h2>Your Card: </h2>
          
          <img src={cardOut("Player")}/> 
        </div>

        <div style={{
          backgroundColor: '#2f3136',
          position: 'absolute',
          right: '30%',
          top: '50%',
          msTransform: "translateY(-50%)",
          transform: "translateY(-50%)",
          paddingLeft: '15px',
          paddingRight: '15px',
          paddingBottom: '5px',
          borderRadius: '10px'
        }}>
          <h2>Player 2 Card: </h2>
          <img src={cardOut("Bot")}/>
        </div>
      </div>
    );
  }
  
  return (
    <div> 
       <div className="container" style={{
        position: 'absolute',
        top: 0,
        left: 0
       }}>

        <div className="tutorials">
          <button onClick={handleOpen}>Rules of Leduc Poker (A bit of a read)</button>
        </div>
        <div className="titleText">
            <h2>Leduc Poker (Practical Research 11S)</h2>
        </div>

        {open && (
          <div>
            <div style={{
              position: 'absolute', 
              top: 0,
              bottom: 0,
              right: 0,
              left: 0, 
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              height: '100vh',
              width: '100%'
            }}></div>

            <div className="popup">
              <div style={{
                position:'absolute',
                left: '77%',
                top: '0%'
              }}>
                <button onClick={handleClose}>Close</button>
              </div>

              <div style={{
                position: 'relative',
                left: '2%'
              }}>
                <h2>Rules of Leduc Poker</h2>

                <p><strong>Cards:</strong> There are only three cards: King (K), Queen (Q), and Jack (J). No suits matter, just the rank.</p>
                <p><strong>Betting:</strong> Each round, you and your opponent throw in some chips (like play money) to start a pot.</p>
                <p><strong>Your Cards:</strong> You each get one card dealt face down (you can't see it). This is your secret weapon!</p>
                <p><strong>Community Card:</strong> One card is flipped face up in the middle for everyone to see.</p>
                <p><strong>Betting Again:</strong> After seeing the community card, you can either raise (bet more chips), call someone else's bet (match it), or fold (give up)</p>
                <p><strong>Winning:</strong> Whoever has the higher-ranking card wins the pot!</p>
                <p>If your secret card matches the community card (e.g., your card is Jack and the community card is Jack), you win!</p>
                <p>If no match, the player with the higher ranking secret card wins (Jack beats Queen, Queen beats King).</p>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <div className="LeducHoldem">
        {gameOver ? (
          <div>
            <div style={{
              position: "absolute",
              left: "50%",
              top: '50%',
              transform: "translate(-50%, -50%)"
            }}>
              <h1>Game Over! {determineWinner()}</h1>
            </div>
            
            <div style={{
              position: 'absolute',
              bottom: '35%',
              left: '50%',
              transform: "translateX(-50%)"
            }}>
              <button onClick={handleNextRound}>Next Round</button>
            </div>
          </div>
          ) : (
          <>
            {!playerCard && 
              <div style={{
                position: "absolute",
                left: "50%",
                top: '60%',
                transform: 'translate(-50%, -50%)',
              }}>
                <button onClick={getData} style={{
                  position: 'fixed',
                  left: '50%',
                  top: '50%',
                  transform: "translate(-50%, -100%)",
                }}>Deal Cards</button>
              </div>
            } 

            {playerCard && (
              <>
                <div
                style={{
                  position: "absolute",
                  left: "50%",
                  top: '10%',
                  transform: "translateX(-50%)"
                }}>
                  <h1>
                    Pot: {botState.pot}
                  </h1>
                </div>
                
                {showCards()}

                {isBettingRound && (
                  <div className='choices' style={{
                    position: 'absolute',
                    bottom: '25%'
                  }}>
                    <button onClick={handleBet}>Bet</button>
                    <button onClick={handleCheck}>Call (Match bet)</button>
                    <button onClick={handleFold}>Fold (Give up)</button>
                  </div> 
                )}
      
                {/* {!isBettingRound && (
                  <>
                    <div style={{
                      position: "absolute",
                      left: "50%",
                      top: '60%',
                      transform: 'translate(-50%, -50%)',
                    }}>
                      <button onClick={getData} style={{
                        position: 'fixed',
                        left: '50%',
                        top: '50%',
                        transform: "translate(-50%, -100%)",
                      }}>Deal Cards</button>
                    </div>
                  </>)
                }  */}
            </>)}
          </>
        )}
      </div>
    </div>
  );
}

export default LeducHoldem;