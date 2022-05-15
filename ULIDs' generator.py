package main

import (
	"ULID-with-sequence-GoLang/crockford"
	"bufio"
	"crypto/rand"
	"fmt"
	"strings"

	"os"
	"strconv"
	"time"
)

func main() {
	fmt.Print("Please enter test duration in seconds: ")
	myScanner := bufio.NewScanner(os.Stdin)
	myScanner.Scan()
	line := myScanner.Text()                    // read the entered duration
	duration, _ := strconv.ParseFloat(line, 64) // convert type string to type float64
	startTime := time.Now().Unix()
	endTime := float64(startTime) + duration // calculate end time

	channel := make(chan string) // create a channel
	counter := 0                 // variable for counting the number of ULID
	go generator(channel)        // start ULID generating

	for float64(time.Now().Unix()) <= endTime { // while the current time less than the end time
		fmt.Println(<-channel) // print next ULID
		counter += 1
	}
	fmt.Println("Seconds per ULID:", duration/float64(counter))
	fmt.Println("Number of ULIDs per second:", float64(counter)/duration)
}

func generator(channel chan string) {
	newSequence := 0
	oldTimestamp := 0

	for newSequence <= 32767 { // serial search of new_sequence
		newTimestamp := int(time.Now().Unix() * 1000)   // timestamp calculation
		newRandomness, _ := rand.Prime(rand.Reader, 65) // randomness calculation
		if oldTimestamp == newTimestamp {               // within a millisecond
			newSequence += 1 // sequence increment
		} else { // new millisecond
			newSequence = 0
		}
		binTimestamp := fmt.Sprintf("%b", newTimestamp) // timestamp to binary system
		binTimestamp = "0000" + binTimestamp
		crockTimestamp := crockford.Encode(binTimestamp) // encode timestamp
		binSequence := fmt.Sprintf("%b", newSequence)    // sequence to binary system
		binSequence = strings.Repeat("0", 15-len(binSequence)) + binSequence
		crockSequence := crockford.Encode(binSequence)     // encode sequence
		binRandomness := fmt.Sprintf("%b", newRandomness)  // randomness to binary system
		crockRandomness := crockford.Encode(binRandomness) // encode randomness
		newUlid := strings.Repeat("0", 10-len(crockTimestamp)) + crockTimestamp +
			strings.Repeat("0", 3-len(crockSequence)) + crockSequence +
			strings.Repeat("0", 13-len(crockRandomness)) + crockRandomness // compose a new ULID

		channel <- newUlid
		oldTimestamp = newTimestamp
	}
	c := 0
	for oldTimestamp == int(time.Now().Unix()*1000) { // wait for the next second
		c += 1
	}
	go generator(channel)
}
