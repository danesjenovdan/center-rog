class Carousel {
  constructor(element) {
    this.board = element;

    // handle gestures
    this.handle();
  }

  getRotation(transformString) {
    const substrings = transformString.match(/rotate\(([^)]+)\)/g);
    for (const substring of substrings) {
      return substring.substring(7, substring.length - 4);
    }
  }

  handle() {
    // list all cards
    this.cards = this.board.querySelectorAll(".studio-card-col");

    // get top card
    this.topCard = this.cards[this.cards.length - 1];

    // get next card
    this.nextCard = this.cards[this.cards.length - 2];

    // if at least one card is present
    if (this.cards.length > 0) {
      const rotation = this.getRotation(this.topCard.style.transform);
      // set default top card position and scale
      this.topCard.style.transform = `translateX(-50%) translateY(-50%) rotate(${rotation}deg) rotateY(0deg) scale(1)`;
      

      // destroy previous Hammer instance, if present
      if (this.hammer) this.hammer.destroy();

      // listen for tap and pan gestures on top card
      this.hammer = new Hammer(this.topCard);

      this.hammer.add(
        new Hammer.Pan({
          position: Hammer.position_ALL,
          threshold: 0,
        })
      );

      // pass events data to custom callbacks
      this.hammer.on("pan", (e) => {
        this.onPan(e);
      });
    }
  }

  onPan(e) {
    
    if (!this.isPanning) {
      this.isPanning = true;

      // remove transition properties
      this.topCard.style.transition = null;
      if (this.nextCard) this.nextCard.style.transition = null;

      // get top card coordinates in pixels
      let style = window.getComputedStyle(this.topCard);
      let mx = style.transform.match(/^matrix\((.+)\)$/);
      this.startPosX = mx ? parseFloat(mx[1].split(", ")[4]) : 0;
      this.startPosY = mx ? parseFloat(mx[1].split(", ")[5]) : 0;

      // get top card bounds
      let bounds = this.topCard.getBoundingClientRect();

      // get finger position on top card, top (1) or bottom (-1)
      this.isDraggingFrom = e.center.y - bounds.top > this.topCard.clientHeight / 2 ? -1 : 1;
    }

    // get new coordinates
    let posX = e.deltaX + this.startPosX;
    let posY = e.deltaY + this.startPosY;

    // get ratio between swiped pixels and the axes
    let propX = e.deltaX / this.board.clientWidth;
    let propY = e.deltaY / this.board.clientHeight;

    // get swipe direction, left (-1) or right (1)
    let dirX = e.deltaX < 0 ? -1 : 1;

    // get degrees of rotation, between 0 and +/- 45
    let deg = this.isDraggingFrom * dirX * Math.abs(propX) * 45;

    // get scale ratio, between .95 and 1
    let scale = (95 + 5 * Math.abs(propX)) / 100;

    // move and rotate top card
    this.topCard.style.transform = "translateX(" + posX + "px) translateY(" + posY + "px) rotate(" + deg + "deg) rotateY(0deg) scale(1)";

    // scale up next card
    if (this.nextCard) {
      const oldNextCardRotation = this.getRotation(this.nextCard.style.transform);
      this.nextCard.style.transform = `translateX(-50%) translateY(-50%) rotate(${oldNextCardRotation}deg) rotateY(0deg) scale(${scale})`;
    }

    if (e.isFinal) {
      this.isPanning = false;

      let successful = false;

      // set back transition properties
      this.topCard.style.transition = "transform 200ms ease-out";
      if (this.nextCard) this.nextCard.style.transition = "transform 100ms linear";

      // check threshold and movement direction
      if (propX > 0.125 && e.direction == Hammer.DIRECTION_RIGHT) {
        successful = true;
        // get right border position
        posX = this.board.clientWidth;
      } else if (propX < -0.125 && e.direction == Hammer.DIRECTION_LEFT) {
        successful = true;
        // get left border position
        posX = -(this.board.clientWidth + this.topCard.clientWidth);
      }

      if (successful) {
        // throw card in the chosen direction
        this.topCard.style.transform = "translateX(" + posX + "px) translateY(" + posY + "px) rotate(" + deg + "deg)";

        // wait transition end
        setTimeout(() => {
          // remove swiped card
          this.board.removeChild(this.topCard);
          // add new card
          this.push(this.topCard);
          // handle gestures on new top card
          this.handle();
        }, 200);
      } else {
        // reset cards position and size
        const randomRotation = Math.floor(Math.random() * 10 - 5);
        this.topCard.style.transform = `translateX(-50%) translateY(-50%) rotate(${randomRotation}deg) rotateY(0deg) scale(1)`;
        if (this.nextCard)  {
          const oldNextCardRotation = this.getRotation(this.nextCard.style.transform);
          this.nextCard.style.transform = `translateX(-50%) translateY(-50%) rotate(${oldNextCardRotation}deg) rotateY(0deg) scale(0.95)`;
        }
      }
    }
  }

  push(element) {
    const randomRotation = Math.floor(Math.random() * 10 - 5);
    element.style.transform = `translateX(-50%) translateY(-50%) rotate(${randomRotation}deg)`;
    this.board.insertBefore(element, this.board.firstChild);
  }
}

(function () {
  // const cards
  let board = document.querySelector(".studios-container-mobile");

  // initial rotations
  const cards = board.querySelectorAll(".studio-card-col");
  for (const card of cards) {
    const randomRotation = Math.floor(Math.random() * 10 - 5);
    card.style.transform = "translateX(-50%) translateY(-50%) rotate(" + randomRotation + "deg)";
  }

  board.addEventListener(
    "animationend",
    function () {
      board.classList.remove("animate");
    },
    false
  );

  let carousel = new Carousel(board);

  let windowHeight;

  function init() {
    windowHeight = window.innerHeight;
  }

  function checkPosition() {
    const positionFromTop = board.getBoundingClientRect().top;

    if (positionFromTop - windowHeight <= -200) {
      board.classList.add("animate");
      window.removeEventListener("scroll", checkPosition);
    }
  }

  window.addEventListener("scroll", checkPosition);
  window.addEventListener("resize", init);

  init();
  checkPosition();
})();




