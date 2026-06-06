
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_033fd058a368e54256cc9a14212fb1ff = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_52f766c863ea72deaec5c3b6dc799f2c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.save_record", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }) }),onClick:on_click_52f766c863ea72deaec5c3b6dc799f2c},children)
    )
});
