import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";
import { useParams, useNavigate } from "react-router-dom";

function CoasterReview({adjustFooterHeight}) {
    function declareHeight(){
		adjustFooterHeight(true)
	}
	useEffect(declareHeight,[])

    const {coasterID} = useParams()
    const {store, actions} = useContext(Context)
    const navigate = useNavigate();

    const [coaster, setCoaster] = useState({})
    const [selectedScore, setSelectedScore] = useState(0)
    const [writtenReview, setWrittenReview] = useState("")

    useEffect(() => {getCoaster()}, [coasterID])

    const url = `${process.env.BACKEND_URL}api/coasters/${coasterID}`

    const getCoaster = () => {
        if (Object.keys(coaster).length > 0) setCoaster({})
        fetch(url, {method: 'GET'})
        .then(response => response.json())
        .then(coaster => setCoaster(coaster))
    }

    const postReview = () => {
        if (selectedScore && writtenReview) {
            fetch(`${process.env.BACKEND_URL}api/review/coaster/${coasterID}`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${store.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    score: selectedScore,
                    review_text: writtenReview
                })
            })
            .then(resp => {
                if (resp.ok) navigate("/userprofile")
            })
        }
        else return console.log("You either didn't score it or didn't right a review");
    }

    const scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    return (
        <div className="container">
            <h2 className="mt-4">Write your review for {coaster["name"]}</h2>
            <div className="mt-5">
                <label className="form-label">
                    <h4>Score:</h4>
                </label>
                <div className="d-flex justify-content-between">
                    {scores.map((value, idx) => {
                        return (
                            <button
                                key={idx}
                                className={`btn ${value > selectedScore ? 'btn-light' : 'btn-primary'} px-4 py-3 shadow`}
                                onClick={() => setSelectedScore(value)}
                            >
                                {value}
                            </button>
                        )
                    })}
                </div>
            </div>
            <div className="mb-3">
                <label htmlFor="scoreexplantion" className="form-label">
                    <h4 className="mt-4">Why did you give it that score?</h4>
                </label>
                <textarea
                    className="form-control"
                    value={writtenReview}
                    placeholder="Write your thoughts here..."
                    id="scoreexplantion"
                    rows="10"
                    onChange={(ev) => setWrittenReview(ev.target.value)}
                ></textarea>
            </div>
            <button
                type="button"
                className="btn btn-success float-end"
                onClick={() => postReview()}
            >
                Post Review
            </button>
        </div>
    )
}
export default CoasterReview